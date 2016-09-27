#coding=utf-8
import sys
from numpy import *
import matplotlib.pyplot as plt

def calculate_distance(v1, v2):
	sum_ans = 0.0
	if len(v1) != len(v2):
		print 'the length of v1&v2 is not same...(let\' go on...)'
	if len(v1) < len(v2):
		v2 = v2[:len(v1)]
		for i in range(len(v1)):
			sum_ans += float((v1[i]-v2[i]))**2.0
	else:
		v1 = v1[:len(v2)]
		for i in range(len(v2)):
			sum_ans += float((v1[i]-v2[i]))**2.0
	sum_ans = sqrt(sum_ans)
	return sum_ans

def init_get_k_centroids(dataSet, k):
	if len(dataSet) < k:
		print "the dataSet is smaller than ", k
		sys.exit()
	k_centroids = []
	for i in range(k):
		k_centroids.append(dataSet[i])
	return k_centroids

def kmeans(dataSet, k):
	dataSet_size = len(dataSet)
	#init the k centroids
	centroids = init_get_k_centroids(dataSet, k)
	distance_list = [sys.maxint]*dataSet_size
	label_list = [-1]*dataSet_size

	cluster_flag = True

	while cluster_flag:
		cluster_flag = False
		#calculate each one data
		for i in range(dataSet_size):
			temp_min_distance = sys.maxint
			temp_label_of_k = -1
			for j in range(k):
				distance = calculate_distance(dataSet[i], centroids[j])
				if distance < temp_min_distance:
					temp_min_distance = distance
					temp_label_of_k = j
			#if the data i's centroid changed
			if temp_label_of_k != label_list[i]:
				distance_list[i] = temp_min_distance**2
				label_list[i] = temp_label_of_k
				cluster_flag = True
		#update the k centroids
		for i in range(k):
			centroids[i] = []
			cc = 0
			for j in range(dataSet_size):
				if label_list[j] == i:
					cc += 1
					if centroids[i] == []:
						centroids[i] = dataSet[j][:]
					else:
						for q in range(len(dataSet[j])):
							centroids[i][q] += dataSet[j][q]
			if cc > 0:
				for q in range(len(centroids[i])):
					centroids[i][q] = float(centroids[i][q]) / float(cc)
		print centroids

	# print "centroids:", centroids
	# print "distance:", distance_list
	# print "label:", label_list
	return label_list, centroids

def create_dataSet(file_path):
	# dataSet = [[1,1],[1,2],[2,1],[2,2],
	# [10,10],[10,11],[11,10],[11,11]]
	dataSet = []
	fr = open(file_path, 'r')
	for line in open(file_path):
		line = fr.readline()
		data = line.strip().split("\t")
		for i in range(len(data)):
			data[i] = float(data[i])
		if len(data) > 0:
			dataSet.append(data)
	return dataSet

def show_matplot(dataSet, label_list, centroids):
	if len(centroids) >= 10:
		print "the number of centroids should be less than 10, because the color is not enougth"
		return 

	if len(dataSet[0]) != 2:
		print "can not draw because the dimension of dataSet is not 2!"
		return 

	mark1 = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
	mark2 = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
	#draw the dataset
	for i in range(len(dataSet)):
		plt.plot(dataSet[i][0], dataSet[i][1], mark1[label_list[i]])
	#draw the centroids
	for i in range(len(centroids)):
		plt.plot(centroids[i][0], centroids[i][1], mark2[i])
	plt.show()
	return 

def train_data(file_train_path, k):
	dataSet = create_dataSet(file_train_path)
	label_list, centroids = kmeans(dataSet, k)
	show_matplot(dataSet, label_list, centroids)
	print "train over..."
	return label_list, centroids

def test_data(file_test_path, centroids):
	dataSet = create_dataSet(file_test_path)
	test_label_list = []
	for data in dataSet:
		max_distance = sys.maxint
		label = -1
		for index in range(len(centroids)):
			temp_distance = calculate_distance(data, centroids[index])
			if temp_distance < max_distance:
				max_distance = temp_distance
				label = index
		test_label_list.append(label)
		print 'data:', data, "; its lable is ", label
	print "test over..."
	return test_label_list


if __name__ == '__main__':
	file_train_path = 'train-kmeans.txt'
	k = 4
	label_list, centroids = train_data(file_train_path, k)
	#if you want to test
	file_test_path = 'test-kmeans.txt'
	test_label_list = test_data(file_test_path, centroids)
	print "all is done..."
