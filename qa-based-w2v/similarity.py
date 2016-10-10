#coding=utf-8

import numpy as np
import gensim
from word_segment import word_segment, filter_word
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class DictObject(object):
	def __init__(self, v):
		self.v = v


def sentence_to_vector(word_list, model):
	s2v = {}
	for w in word_list:
		if w in model.vocab:
			s2v[w] = DictObject(model[w].tolist())
	return s2v


'''
return np.float64
'''
def calculate_cos_2_list(dict1, dict2):
	#union 2 dict
	all_dict = {}
	for d in dict1.items():
		if d[0] not in all_dict:
			all_dict[d[0]] = 1
	for d in dict2.items():
		if d[0] not in all_dict:
			all_dict[d[0]] = 1
	v1 = []
	for d in all_dict:
		if d in dict1:
			v1.append(dict1[d].v)
		else:
			v1.append([0.0]*len(dict2[d].v))
	v2 = []
	for d in all_dict:
		if d in dict2:
			v2.append(dict2[d].v)
		else:
			v2.append([0.0]*len(dict1[d].v))
	#cos
	si = np.float64(0)
	for i in range(len(v1)):
		x = np.array(v1[i])
		y = np.array(v2[i])
		xx = np.sqrt(x.dot(x))
		yy = np.sqrt(y.dot(y))
		if xx * yy != np.float64(0):
			si += (x.dot(y) / (xx * yy))
	return si


#First: load model
model = gensim.models.Word2Vec.load('localfile/model/5_300_5.model')
#Second: word segment
word_segment(old_file_path='localfile/querySentence.txt',
			 new_file_path='localfile/querySentenceWords.txt',
			 user_dict_path='localfile/mydict.dic',
			 stopword_dict_path='localfile/stopword.dic')
filter_word(file_path='localfile/querySentenceWords.txt',
			filter_file_path='localfile/filterword.txt',
			new_file_path='localfile/filteredQuerySentenceWords.txt')
query = ""
with open('localfile/querySentence.txt', 'rb') as fopr:
	for line in fopr:
		if line != "":
			query = line.decode('utf-8', 'ignore')
			break
query_w_list = []
with open('localfile/filteredQuerySentenceWords.txt', 'r') as fopr:
	for line in fopr:
		query_w_list = line.strip().split(" ")
		break
#Third: calculate
sentences = []
with open('localfile/allhtmlcontent.txt', 'r') as fopr:
	for line in fopr:
		if line != "":
			sentences.append(line.strip())

with open('localfile/wordallfilterhtmlcontent.txt', 'r') as fopr:
	max_similarity = np.float64(0)
	max_index = 0
	cur_similarity = np.float64(0)
	cur_index = 0
	s2v_of_query_w_list = sentence_to_vector(query_w_list, model)
	#print s2v_of_query_w_list['什么'].tolist()
	for line in fopr:
		if line != "":
			w_list = line.strip().split(" ")
			s2v_of_cur_w_list = sentence_to_vector(w_list, model)
			cur_similarity = calculate_cos_2_list(s2v_of_query_w_list, s2v_of_cur_w_list)
			if cur_similarity > max_similarity:
				max_similarity = cur_similarity
				max_index = cur_index
			print '[', cur_index, ']', 'max_similarity = ', max_similarity
			cur_index += 1
	print '\nthe query is:', query
	print '[', max_index, '] is:', sentences[max_index].encode('gbk', 'ignore')