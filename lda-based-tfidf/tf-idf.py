#coding=utf-8

from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import jieba, sys, os
import jieba.analyse
import numpy as np


'''
get file content
'''
def get_file_content(file_path):
	fopen = open(file_path, 'rb')
	content = fopen.read()
	return content.decode('utf-8', 'ignore')


'''
conver the corpus file to tf-idf array
para: the file's path
	   the file's content: 1. one line is one sentence
						   2. the sentence must be word segment
						   3. for example: "a is b and c ." and Chinese is the same
return: x_array just like [[1,2,3...],[1,2,3...]...]
		 x_name [word1,word2...wordN]
'''
def get_array(file_path):
	print ('start get x array from corpus...')
	vectorizer = CountVectorizer()
	fopen = open(file_path, 'rb')
	corpus = []
	for line in open(file_path,'rb'):
		line = fopen.readline()
		line = line.strip()
		corpus.append(line)
	fopen.close()
	x1 = vectorizer.fit_transform(corpus)
	x_array = x1.toarray()
	x_name = vectorizer.get_feature_names()
	print ('ok...\n')
	return x_array, x_name


'''
filter some not important words(the idf's value is small)
para: the tf-idf array( that is x_array)
'''
def filter_x_array(x_array, tf_idf_minin_value):
	x_array = x_array.tolist()
	print 'start filter x_array...'
	#init
	x_array_sum = []
	col_array = 0
	for one_array in x_array:
		col_array = len(one_array)
		for i in range(col_array):
			x_array_sum.append(int(0))
		break
	#get the x_array's sum
	#x_array_sum is one dimension
	for one_array in x_array:
		for index in range(len(one_array)):	
			x_array_sum[ index ] += one_array[index]
	#start filter 
	myDict = {}
	for i in range(len(x_array_sum)):
		if x_array_sum[i] < tf_idf_minin_value:
			myDict[i] = i
	row_array = len(x_array)
	print "row = "+str(row_array)+" ;col = "+str(col_array)
	for i in range(row_array):
		for j in range(col_array-1, -1 ,-1):
			if j in myDict:
				#print "j is ",j
				#x_array[i][j] = 0
				x_array[i].pop(j)
	row_array = len(x_array)
	col_array = 0
	for one_array in x_array:
		if col_array==0:
			col_array = len(one_array)
		else:
			if col_array != len(one_array):
				print "tf-idf array: cannot erase success(as for one col)!!!!!"
				sys.exit('Oh, my god! ERROR!')
	print "new_row = "+str(row_array)+" ;new_col = "+str(col_array)
	print ('ok...\n')
	return np.array(x_array)


'''
get tf-idf weight
para: x_array:[[1,2,3...],[1,2,3...]...]
return: [[0.1,0.2,0.3...],[0.2,0.1,...]...]
'''
def get_tf_idf(x_array):
	print ('start get tf-idf array...')
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(x_array)
	tfidf_array = tfidf.toarray()
	print ('ok...\n')
	return tfidf_array


'''
write something to local file
para: x is [[1,2,3...],[1,2,3...]...]
	   file_path: the dst file path
'''
def write_all_thing(x1, file_path):
	print ('start write '+file_path+' into local file...')
	fopenw = open(file_path,'w')
	print ('the array size is '+str(len(x1)))
	for x2 in x1:
		cnt = 0
		for x3 in x2:
			if cnt==0 :
				fopenw.write(str(x3))
			else:
				fopenw.write(' '+str(x3))
			cnt += 1
		fopenw.write('\n')
	fopenw.close()
	print ('ok...')


if __name__ == '__main__':
	
	file_path = "localfile/wordallfilterhtmlcontent.txt"
	result_file_path = 'localfile/x_array.txt'
	tf_idf_minin_value = 5

	if len(sys.argv) >= 4:
		file_path = sys.argv[1]
		result_file_path = sys.argv[2]
		tf_idf_minin_value = sys.argv[3]
		#get tf-idf array
		x_array, x_name = get_array(file_path)
		#delete the array's cols which are 0
		x_array = filter_x_array(x_array, int(tf_idf_minin_value))
		#get tf-idf weight array
		tfidf_array = get_tf_idf(x_array)
		#write some thing
		write_all_thing(x_array, result_file_path)
		#write_all_thing(tfidf_array, "localfile/tfidf_array.txt")
	else:
		print '[ERROR] check the file & value'
	print('\nfinish...\n')
