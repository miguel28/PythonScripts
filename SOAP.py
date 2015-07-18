import time
import urllib
import httplib
from lxml.etree import XML, tostring, _ElementTree, XMLSchema

def decode_arrayofstring(l):
    if not isinstance(l, (list, tuple, set)):
        raise TypeError('parameter must be a list of strings')
    if not len(l):
        raise TypeError('parameter cannot be empty')
    for s in l:
        if not isinstance(s, (str, unicode)):
            raise TypeError('parameter must be a list of string, found %s' % type(s))
    return '<string>' + '</string><string>'.join(l) + '</string>'

SOAPTypes = dict(
    boolean=(bool, lambda s: str(s).lower().strip()=='true'),
    int=(int, int),
    double=(float, float),
    string=(str, str),
    xml=(_ElementTree, tostring),
    arrayofstring=(list, decode_arrayofstring)
)

class ServiceExcept(Exception):
    pass

class Client:
    def __init__(self, host, url):
        self._url = url
        self._host = host
        self._methods = {}
        if not url.lower().endswith('?wsdl'):
            self._url += '?WSDL'
        httpconn = httplib.HTTPConnection(self._host)
        httpconn.request('GET', self._url)
        f = httpconn.getresponse()
        wsdl = XML(f.read())
        f.close()
        httpconn.close()
        self._nameSpace = wsdl.xpath('@targetNamespace', namespaces=wsdl.nsmap, smart_strings=False)[0]
        try:
            service_name = wsdl.xpath(
                "/wsdl:definitions/wsdl:service/@name",
                namespaces=wsdl.nsmap,
                smart_strings=False,
            )[0]
        except IndexError:
            raise ServiceExcept('Unable to find Service Name.')
        for operation in wsdl.xpath(
                        "/wsdl:definitions/wsdl:binding[@name='%sSoap12' or @name='%sSoap']/wsdl:operation" % (service_name, service_name),
                        namespaces=wsdl.nsmap,
                        smart_strings=False,
                    ):
            name = operation.xpath('@name', smart_strings=False)[0]
            soapAction = operation.xpath('*/@soapAction', smart_strings=False)[0]
            inputName = wsdl.xpath("/wsdl:definitions/wsdl:portType/wsdl:operation[@name='%s']/wsdl:input/@message" % name, namespaces=wsdl.nsmap, smart_strings=False)[0]
            outputName = wsdl.xpath("/wsdl:definitions/wsdl:portType/wsdl:operation[@name='%s']/wsdl:output/@message" % name, namespaces=wsdl.nsmap, smart_strings=False)[0]
            inputName, outputName = inputName[inputName.find(':')+1:], outputName[outputName.find(':')+1:]
            inputMessage = wsdl.xpath("/wsdl:definitions/wsdl:message[@name='%s']/wsdl:part[@name='parameters']/@element" % inputName, namespaces=wsdl.nsmap, smart_strings=False)[0]
            outputMessage = wsdl.xpath("/wsdl:definitions/wsdl:message[@name='%s']/wsdl:part[@name='parameters']/@element" % outputName, namespaces=wsdl.nsmap, smart_strings=False)[0]
            inputMessage, outputMessage = inputMessage[inputMessage.find(':')+1:], outputMessage[outputMessage.find(':')+1:]
            params = []
            ret = None
            for node in  wsdl.xpath("/wsdl:definitions/wsdl:types/s:schema/s:element[@name='%s']/s:complexType/s:sequence/s:element" % inputMessage, namespaces=wsdl.nsmap):
                pname = node.xpath('@name', smart_strings=False)[0]
                try:
                    _type = node.xpath('@type', smart_strings=False)[0]
                    _type = _type[_type.index(':')+1:].lower().strip()
                    params.append((pname, SOAPTypes[_type]))
                except IndexError:
                    params.append((pname, SOAPTypes['xml']))
                
            retName = wsdl.xpath("/wsdl:definitions/wsdl:types/s:schema/s:element[@name='%s']/s:complexType/s:sequence/s:element/@name" % outputMessage, namespaces=wsdl.nsmap, smart_strings=False)[0]
            try:
                ret = wsdl.xpath("/wsdl:definitions/wsdl:types/s:schema/s:element[@name='%s']/s:complexType/s:sequence/s:element/@type" % outputMessage, namespaces=wsdl.nsmap, smart_strings=False)[0]
                ret = ret.replace('s:','').lower().strip()
            except IndexError:
                ret = 'complex'
                
            self._methods[name] = dict(
                soapAction=soapAction,
                inputMessage=inputMessage,
                outputMessage=outputMessage,
                params=params,
                retName=retName,
                ret=ret,
            )
        
        del wsdl
        
    def _makeBodyResponse(self, inputMessage, params, args, kwargs):
        nameSpace = self._nameSpace
        params_string = ''
        for k, v in params:
            if k not in kwargs:
                raise Exception('Parameter %s is missing' % k)
            params_string += '<%s>%s</%s>' % (k, str(v[1](kwargs[k])), k)
        body = '''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <%(inputMessage)s xmlns="%(nameSpace)s">
                    %(params_string)s
                </%(inputMessage)s>
            </soap:Body>
        </soap:Envelope>''' % locals()
        return body
        
    def _call_remote(self, soapAction, body, outputMessage, retName, ret):
        headers = {
            'Host': self._host,
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': str(len(body)),
            'SOAPAction': '"%s"' % soapAction,
        }
        httpconn = httplib.HTTPConnection(self._host)
        httpconn.request('POST', self._url, body=body, headers=headers)
        r = httpconn.getresponse()
        d = r.read()
        if r.status == 500:
            if '<faultstring>' in d:
                d = d[d.index('<faultstring>')+len('<faultstring>'):]
                d = d[:d.index('</faultstring>')]
                raise ServiceExcept('WebService Exception server(%s) Action(%s) message(%s)' % (self._host, soapAction, d))
        elif r.status != 200:
            raise ValueError('Error connecting: %s, %s, %s' % (r.status, r.reason, str(d)))
        result = XML(d)
        d = result.nsmap.copy()
        d['gbl'] = self._nameSpace
        retNode = result.xpath('/soap:Envelope/soap:Body/gbl:%s/gbl:%s' % (outputMessage, retName), namespaces=d)[0]
        if ret == 'complex':
            return retNode
        return retNode.text
        
    def __getattr__(self, name):
        if name not in self._methods:
            raise AttributeError(name)
        m = self._methods[name]
        def remote_method(*args, **kwargs):
            body = self._makeBodyResponse(m['inputMessage'], m['params'], args, kwargs)
            return self._call_remote(m['soapAction'], body, m['outputMessage'], m['retName'], m['ret'])
        return remote_method