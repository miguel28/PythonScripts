import pdb
#from scipy.spatial import distance
class Coord():
	def __init__(self, value, key):
		self.value = value
		self.key = key

def order_points(point_list):
	order_map = {}
	x_list = []
	x_list2 = []
	ordered_list = []
	i = 0
	for point in point_list:
		order_map[i] = point
		coord = Coord(point[0], i)
		x_list.append(coord)
		x_list2.append(point[0])
		i += 1
	x_list.sort(key=lambda x: x.value)
	x_list2.sort()
	i = 0
	num = len(x_list2)
	repeated_indexes = []
	while i < num - 1:
		if x_list2[i] == x_list2[i + 1]:
			repeated_indexes.append(i)
		i += 1 
	for x in x_list:
		ordered_list.append(order_map[x.key])
	for index in repeated_indexes:
		point1 = ordered_list[index]
		point2 = ordered_list[index + 1]
		if point1[1] > point2[1]:
			ordered_list[index] = point2
			ordered_list[index + 1] = point1
	return ordered_list

point_list1 = [[459, 120], [148, 126],[85, 263],[145, 395], [460, 397], [480, 258]]
point_list2 = [[141,120],[84, 258],[138, 388],[449, 393],[478, 267],[454, 120]]
#point_list3 = [[460, 120],[460, 60],[460, 118]]
point_list1 = order_points(point_list1)
point_list2 = order_points(point_list2)
#point_list3 = order_points(point_list3)
print point_list1
print point_list2
#print point_list3
#print distance.euclidean(point_list1, point_list2)
raw_input("Press key...")
