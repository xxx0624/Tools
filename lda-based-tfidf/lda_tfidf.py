#coding=utf-8

import numpy, types
import lda
import lda.datasets
import codecs
import sys, os
import numpy as np
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
			x_array_sum[ index ] += int(one_array[index])
	#start filter 
	myDict = {}
	for i in range(len(x_array_sum)):
		if x_array_sum[i] <= tf_idf_minin_value:
			myDict[i] = i
	print "x_array:row is "+str(len(x_array))+"; col is "+str(col_array)
	print "x_name:len is "+str(len(x_name))
	#filter xname
	for i in range(len(x_name)-1, -1, -1):
		if i in myDict:
			x_name.pop(i)
	#filter xarray
	new_x_array = []
	col_new_array = 0
	for one_array in x_array:
		col_new_array = 0
		for i in range(len(one_array) - 1, -1, -1):
			if i in myDict:
				one_array.pop(i)
			else:
				col_new_array += 1
		for i in range(len(one_array)):
			one_array[i] = int(one_array[i])
		new_x_array.append(one_array)
	print "new_x_array:row is "+str(len(new_x_array))+"; col is "+str(col_new_array)
	print "new_x_name:len is "+str(len(x_name))
	print 'ok...\n'
	return new_x_array, x_name


'''
get the vocab
'''
def get_array(file_path):
	print ('start get array from corpus...')
	vectorizer = CountVectorizer()
	#transformer = TfidfTransformer()
	fopen = codecs.open(file_path, 'r')
	corpus = []
	for line in codecs.open(file_path, 'r'):
		line = fopen.readline()
		line = line.strip()
		corpus.append(line)
	#print corpus
	fopen.close()
	x1 = vectorizer.fit_transform(corpus)
	#tfidf = transformer.fit_transform(x1)
	#weight = tfidf.toarray()
	x_array = x1.toarray()
	x_name = vectorizer.get_feature_names()
	print "x_name len = ", len(x_name)
	print 'x_array len = ', len(x_array)
	print 'ok...\n'
	return x_array, x_name


'''
get lda's result (such as:topics, components)
para: file_path is the x_array(that is tf-idf)'s file 
			one row is one doc and one col is the number of the word
return: the topics 
			one row is one doc and one col is one P 
'''
def lda_solve(filter_file_path, show_topic_word_num = 1, n_topics=20, random_state=1, n_iter=500):
	print ("\nstart get the topics...")

	X, temp_vocab = get_array(filter_file_path)
	X, temp_vocab = filter_x_name(X, temp_vocab, 5)

	X = numpy.array(X)
	model = lda.LDA(n_topics=n_topics, random_state=random_state, n_iter=n_iter)
	model.fit(X)

	#tempX, temp_vocab = get_array(filter_file_path)
	#temp_vocab = filter_x_name(tempX, temp_vocab, 5)
	#print vocab
	vocab = tuple(temp_vocab)
	topic_word = model.topic_word_
	topic_word_score = []
	for i, topic_dist in enumerate(topic_word):
		topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]
		topic_words_score = topic_dist[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]
		#print ('topic {0}:{1}'.format(i, u' '.join(topic_words).encode('utf-8')))
		#print ('topic score:'+str(topic_dist[numpy.argsort(topic_dist)][:-(show_topic_word_num+1):-1]))
	'''
	print "===== mode.doc_topic_ ====="
	print len(model.doc_topic_), len(model.doc_topic_[0])
	print model.doc_topic_
	print "============\n"
	print "===== model.topic_word_ ====="
	print len(topic_word), len(topic_word[0])
	print topic_word
	print "============"
	'''
	print ("ok...\n")
	return model.doc_topic_, model.topic_word_, vocab, model.loglikelihoods_


'''
write two dimesion into local file
'''
def write_local_file(arr, new_file_path):
	print ("====== start write "+str(new_file_path)+" into localfile ======")
	if os.path.exists(new_file_path) == False:
		print("dont find the file...\nstart create the file...")
		f = open(new_file_path, 'w')
		f.close()
		print("create the file successfully...")
	fopenw = open(new_file_path, 'w')
	for x in arr:
		temp = ""
		index = 1
		max_value_index = -1
		max_value = -1.0
		for y in x:
			if max_value < float(y):
				max_value = float(y)
				max_value_index = index
			if temp == "":
				temp = str(y)
			else:
				temp = temp + "," + str(y)
			index += 1
		fopenw.write(str(max_value_index) + ',' + temp)
		fopenw.write('\n')
	fopenw.close()
	print ("====== ok ======\n")


def write_local_file(doc_topic, topic_word, vocab, show_topic_word_num, log_likelihoods, sentences_file_path='localfile/allhtmlcontent.txt', file_path='localfile/finalResult/finalResult.txt'):
	print "====== start write "+str(file_path)+"...  ======"

	doc_word = np.dot(np.matrix(doc_topic), np.matrix(topic_word))

	sentences = []
	fr = open(sentences_file_path, 'rb')
	for line in fr:
		if line.strip() == "":
			continue
		sentences.append(line.strip())
	fr.close()

	fw = open(file_path, 'w')
	fw.write("log_likelihoods: " + str(log_likelihoods) + "\n\n")
	for sentence_id in range(len(doc_word)):
		word_list = numpy.array(doc_word)[sentence_id].tolist()
		words = {}
		for i in range(len(word_list)):
			words[i] = word_list[i]
		words = sorted(words.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
		#print type(words)
		fw.write(sentences[sentence_id] + "\n")
		sentence_id += 1
		for i in range(show_topic_word_num):
			fw.write(vocab[int(words[i][0])] + " ")
		fw.write("\n")
		for i in range(show_topic_word_num):
			fw.write(str(words[i][1]) + " ")
		fw.write("\n\n")
	fw.close()
	
	print "====== ok ======"


#todo
def likelihood_best():
	pass


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
	print "====== ok ======\n"
	fopenw.close()


if __name__ == "__main__":
	filter_file_path = 'localfile/wordallfilterhtmlcontent.txt'
	show_topic_word_num = 5

	n_topics = 20
	random_state = 1
	n_iter = 500

	for n_topics in range(5, 200, 5):
		for random_state in range(0, 2, 1):
			for n_iter in range(50, 1000, 10):
				doc_topic, topic_word, vocab, log_likelihoods = lda_solve(filter_file_path, show_topic_word_num=show_topic_word_num, n_topics=n_topics, random_state=random_state, n_iter=n_iter)

				#record some thing
				#write_local_file(doc_topic, 'localfile/doc_topic.csv')
				#write_local_file(topic_word, 'localfile/topic_word.csv')
				#write_doc_score_to_localfile(topic_word, vocab, 'localfile/topic_word_score.csv')
				write_local_file(doc_topic, topic_word, vocab, show_topic_word_num, log_likelihoods,
								 file_path="localfile/finalResult/finalResult"+str(n_topics)+"_"+str(random_state)+"_"+str(n_iter)+"_"+str(show_topic_word_num)+".txt" )

	print 'finish...'
