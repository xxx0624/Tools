# -*- coding: utf-8 -*-

import os, sys
import gensim

class MySentence(object):
	def __init__(self, file_path):
		self.file_path = file_path

	def __iter__(self):
		if os.path.isfile(self.file_path):
			with open(self.file_path, 'r') as fopr:
				for words in fopr:
					words = words.strip()
					yield words.split(' ')

if __name__ == "__main__":
	print 'start train model...'
	sentences = MySentence('localfile/wordallfilterhtmlcontent.txt')
	min_count = 5
	workers = 5
	size = 300
	window = 5
	model = gensim.models.Word2Vec(sentences=sentences,
								   min_count=min_count,
								   workers=workers,
								   size=size,
								   window=window
								   )

	model.save('localfile/model/' + str(min_count) + "_" + str(size) + "_" + str(window) + ".model")
	model.save_word2vec_format('localfile/model/' + str(min_count) + "_" + str(size) + "_" + str(window) + "_w2v.model", binary=False)
	print 'finish...'
