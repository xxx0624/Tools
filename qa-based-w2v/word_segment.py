#coding=utf-8

import jieba, time
import jieba.analyse


def comp(a, b):
	if (a > b) - (a < b):
		return False
	else:
		return True


def check_file_name(filename):
	if filename is None or filename == "":
		return False
	else:
		return True


def judge_word_allnumoralpa(word):
	flag = True
	for i in range(len(word)):
		if (word[i] >= '0' and word[i] <= '9') or (word[i] >= 'a' and word[i] <= 'z') or (word[i] >= 'A' and word[i] <= 'Z'):
			pass
		else:
			flag = False
	return flag


def judge_word_all_punctuation(word):
	flag = True
	for i in range(len(word)):
		if word[i] == '.' or word[i] == '?' or word[i] == ',' or word[i] == '？' or word[i] == '。' or word[i] == '，':
			pass
		else:
			flag = False
	return flag


def word_segment(old_file_path, new_file_path, user_dict_path, stopword_dict_path):
	if False == (check_file_name(old_file_path) and check_file_name(new_file_path)) :
		print '[ERROR] check the file1 & file2...'
		return -1
	if check_file_name(user_dict_path) == True:
		jieba.load_userdict(user_dict_path)
	if check_file_name(stopword_dict_path) == True:
		jieba.analyse.set_stop_words(stopword_dict_path)
	fopenr = open(old_file_path, 'rb')
	fopenw = open(new_file_path, 'w')
	line_no = 1
	for line in open(old_file_path, 'rb'):
		line = fopenr.readline()
		line = line.decode('utf-8', 'ignore')
		line = line.strip()
		line_no += 1
		seg_list = jieba.cut(line, cut_all = False)
		cnt = 0
		cnt_special = 0
		line_word = ""
		for seg in seg_list:
			if comp('\n', seg) or comp("\n\n", seg) or comp("\r", seg) or comp("\r\n", seg) or comp("\t", seg) or seg == "":
				cnt_special += 1
			else:
				#get word segment
				if line_word == "":
					line_word = seg
				else:
					line_word = line_word + " "+seg
				#print str(cnt)+":",(seg.strip())
				cnt += 1
		print "[", line_no, "] size:", cnt
		#print ("special size:"+str(cnt_special))
		#write the word segment into new file
		line_word = line_word.encode('utf-8')
		fopenw.write(line_word)
		fopenw.write('\n')
	fopenr.close()
	fopenw.close()


'''
filter word in filter_file_path & filter words whos' len no more than 1
'''
def filter_word(file_path, filter_file_path, new_file_path):
	#read filter file
	fopenr = open(filter_file_path, 'rb')
	filter_dict = {}
	for line in open(filter_file_path, 'rb'):
		line = line.strip().decode('utf-8', 'ignore')
		filter_dict[line] = line
	fopenr.close()

	#start filter file
	cnt_filter = 0
	fopenr = open(file_path, 'rb')
	fopenw = open(new_file_path, 'w')
	for line in open(file_path, 'rb'):
		line = fopenr.readline()
		line = line.strip().decode('utf-8', 'ignore')
		line_word_list = line.split(' ')
		new_line = ""
		for line_word in line_word_list:
			line_word = line_word.strip()
			if line_word in filter_dict or len(line_word) <= 1:
				cnt_filter += 1
				#pass
			#elif judge_word_allnumoralpa(line_word) == True:
			#	cnt_filter += 1
			#	pass
			else:
				if new_line == "":
					new_line = line_word
				else:
					new_line = new_line + " " + line_word
		fopenw.write(new_line.encode('utf-8'))
		fopenw.write('\n')
	print 'all filtered words\' size = ', cnt_filter
	fopenw.close()
	fopenr.close()


if __name__ == '__main__':

	file1 = 'localfile/allhtmlcontent.txt'
	file2 = 'localfile/wordallhtmlcontent.txt'
	file3 = 'localfile/filterword.txt'
	file4 = 'localfile/wordallfilterhtmlcontent.txt'
	file5 = 'localfile/mydict.dic'
	file6 = 'localfile/stopword.dic'

	word_segment(file1, file2, file5, file6)
	filter_word(file2, file3, file4)

	print 'finish...'