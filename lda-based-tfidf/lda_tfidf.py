#coding=utf-8

import numpy, types
import lda
import lda.datasets
import codecs
import sys, os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

reload(sys)
sys.setdefaultencoding('utf-8')

'''
filter some not important words(the idf's value is small)
para: the tf-idf array( that is x_array)
	  one row word(that is x_name)
'''
def filter_x_name(x_array, x_name, tf_idf_minin_value):
	x_array = x_array.tolist()
	print ('start filter x_name...')
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
	print "x_array:row is "+str(row_array)+"; col is "+str(col_array)
	print "x_name:len is "+str(len(x_name))
	for i in range(len(x_name)-1, -1, -1):
		if i in myDict:
			x_name.pop(i)
	row_array = len(x_array)
	col_array = 0
	print "new x_name:len is "+str(len(x_name))
	print 'ok...\n'
	return x_name


'''
get the vocab
'''
def get_array(file_path):
	print ('start get array from corpus...')
	vectorizer = CountVectorizer()
	transformer = TfidfTransformer()
	fopen = codecs.open(file_path, 'r')
	corpus = []
	for line in codecs.open(file_path, 'r'):
		line = fopen.readline()
		line = line.strip()
		corpus.append(line)
	#print corpus
	fopen.close()
	x1 = vectorizer.fit_transform(corpus)
	tfidf = transformer.fit_transform(x1)
	weight = tfidf.toarray()
	x_array = x1.toarray()
	x_name = vectorizer.get_feature_names()
	print "x_name's len = ", len(x_name)
	print 'ok...\n'
	return x_array, x_name


'''
get lda's result (such as:topics, components)
para: file_path is the x_array(that is tf-idf)'s file 
			one row is one doc and one col is the number of the word
return: the topics 
			one row is one doc and one col is one P 
'''
def lda_solve(file_path, show_topic_word_num = 1, n_topics=5, random_state=0, n_iter=50):
	print ("\nstart get the topics...")
	fopenr = open(file_path, 'r')
	X = []
	index = 1
	for line in open(file_path, 'r'):
		index += 1
		line = fopenr.readline()
		if line == "":
			continue
		line = line.strip().split(' ')
		cnt = 0
		for w in line:
			line[cnt] = int(w)
			cnt += 1
		X.append(line)
	fopenr.close()
	X = numpy.array(X)
	model = lda.LDA(n_topics = n_topics, random_state = random_state, n_iter = n_iter)
	model.fit(X)
	print ("ok...\n")
	tempX, temp_vocab = get_array('localfile/wordallfilterhtmlcontent.txt')
	temp_vocab = filter_x_name(tempX, temp_vocab, 5)
	#print vocab
	vocab = tuple(temp_vocab)
	topic_word = model.topic_word_
	topic_word_score = []
	for i, topic_dist in enumerate(topic_word):
		topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]
		topic_words_score = topic_dist[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]
		print ('topic {0}:{1}'.format(i, u' '.join(topic_words).encode('utf-8')))
		print ('topic score:'+str(topic_dist[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]))
	print "=====mode.doc_topic_====="
	print model.doc_topic_
	print "============\n"
	print "=====model.topic_word_====="
	print topic_word
	print "============"
	return model.doc_topic_, model.topic_word_, vocab


'''
write two dimesion into local file
'''
def write_local_file(arr, new_file_path):
	print ("\nstart write "+str(new_file_path)+" into local...")
	if os.path.exists(new_file_path) == False:
		print("dont find the file...\nstart create the file...")
		f = open(new_file_path, 'w')
		f.close()
		print("create the file successfully...")
	fopenw = open(new_file_path, 'w')
	for x in arr:
		temp = ""
		for y in x:
			if temp == "":
				temp = str(y)
			else:
				temp = temp + "," + str(y)
		fopenw.write(temp)
		fopenw.write('\n')
	fopenw.close()
	print ("ok...\n")


'''
'''
def write_doc_score_to_localfile(topic_word, vocab, new_file_path):
	print "====== write_doc_score_to_localfile ====="
	fopenw = open(new_file_path, 'wb')
	show_topic_word_num = 10
	for i, topic_dist in enumerate(topic_word):
		topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]
		topic_words_score = topic_dist[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]
		flag = 0
		for w in topic_words:
			if flag == 0:
				fopenw.write(str(w).encode('gbk'))
				flag = 1
			else:
				fopenw.write(',')
				fopenw.write(str(w).encode('gbk'))
		fopenw.write('\n')
		flag = 0
		for s in topic_words_score:
			if flag == 0:
				fopenw.write(str(s))
				flag = 1
			else:
				fopenw.write(',')
				fopenw.write(str(s))
		fopenw.write('\n')
	print "====== ok ========="
	fopenw.close()


if __name__ == "__main__":
	file1 = 'localfile/x_array.txt'
	show_topic_word_num = 3
	n_topics = 20
	random_state = 1
	n_iter = 500
	if len(sys.argv) >= 2:
		file1 = sys.argv[1]
		if len(sys.argv) >= 3:
			show_topic_word_num = int(sys.argv[2])
		if len(sys.argv) >= 4:
			n_topics = int(sys.argv[3])
		if len(sys.argv) >= 5:
			random_state = int(sys.argv[4])
		if len(sys.argv) >= 6:
			n_iter = int(sys.argv[5])
		doc_topic, topic_word, vocab = lda_solve(file1, show_topic_word_num = show_topic_word_num, n_topics=n_topics, random_state=random_state, n_iter=n_iter)
		#write_local_file(doc_topic, 'localfile/doc_topic.csv')
		#write_local_file(topic_word, 'localfile/topic_word.csv')
		#write_doc_score_to_localfile(topic_word,vocab, 'localfile/topic_word_score.csv')
	else:
		print '[ERROR] check the file & value'
	print 'finish...'