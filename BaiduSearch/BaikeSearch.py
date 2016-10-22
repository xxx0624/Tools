#coding=utf-8

import sys
from bs4 import BeautifulSoup as bs
import urllib2 as url
import chardet, codecs

reload(sys)
sys.setdefaultencoding('utf-8')


baike_link = "http://baike.baidu.com/item/"
baike_search_link = 'http://baike.baidu.com/search?word='
baike_detail_prelink = 'http://baike.baidu.com'


def get_html_content(url_link):
	try:
		res = url.urlopen(url_link, timeout=100)
		return res.read()
	except:
		return None
		#print 'ex', url_link


def clean_html(html_url):
	html_content = get_html_content(html_url)
	if html_content is None:
		return None
	soup = bs(html_content, 'lxml').find('body')
	if soup is None:
		p1 = html_content.find('<body')
		p2 = html_content.find('</body>')
		if p1 < 0 or p2 < 2:
			return None
		soup = bs(html_content[p1: p2+7], 'lxml')
	if soup is None:
		return None
	to_extract = soup.findAll('script')
	for it in to_extract:
		it.extract()
	res = soup.get_text()\
		.replace('\n', '')\
		.replace('\t', '')\
		.replace('\r', '')\
		.replace('百度', '')\
		.strip()
	res = res[160:]
	res = res[:-200]
	return res


def search_baike_item(words):
	#split keywords
	keywords = ""
	details = ""
	if '(' in words or '（' in words:
		left_pos = words.find('(')
		right_pos = words.find(')')
		keywords = words[:left_pos]
		details = words[left_pos + 1:right_pos]
	else:
		keywords = words

	keywords = keywords.replace(' ', '+')
	baidu_html_content = get_html_content(baike_search_link + keywords+'&pn=0&rn=0&enc=utf8')
	if baidu_html_content is None:
		return None

	#1.parse baidu's url to get baike's url
	soup = bs(baidu_html_content, 'lxml')
	items = soup.find_all(['a'], {'class':'result-title'})
	baike_item_link = ""
	if len(items) > 0:
		for item in items:
			baike_item_link = item.get('href')
			break
	else:
		#no baike
		return -1
	#2.parse baike's url to get if exist many same items
	baike_html_content = get_html_content(baike_item_link)
	if baike_html_content is None:
		return None
	soup = bs(baike_html_content, 'lxml')
	items = soup.find_all(['ul'], {'class':'polysemantList-wrapper cmn-clearfix'})
	if len(items) > 0:
		soup = bs(str(items[0]), 'lxml')
		items = soup.find_all(['li'])
		for i in range(len(items)):
			if details in str(items[i]) or str(items[i]) in details:
				if '<a ' in str(items[i]):
					#a_item = bs(str(items[i]), 'lxml').find_all(['a'])[0].get('href')
					a_item = bs(str(items[i].contents), 'lxml').find_all(['a'])[0].get('href')
					return baike_detail_prelink + a_item
				if '<span ' in str(items[i]):
					#信息就在本页面
					return baike_item_link
				'''
				with open('result2.txt', 'w') as f:
					f.write(clean_html(get_html_content(baike_detail_prelink+a_item)))
				'''
		#no choice
		for i in range(len(items)):
			if '<span ' in str(items[i]):
				#返回本页面
				return baike_item_link
	else:
		#信息就在本页面
		return baike_item_link


def get_baike_search_result(keywords):
	while True:
		#get baike's url
		res_url = search_baike_item(keywords)
		if res_url == -1:
			return -1
		if res_url is None:
			continue
		#get html content
		res_content = html_content(res_url)
		if res_content is None:
			#get html content error
			return -1
		#ok
		return res_content
	return -1


if __name__ == "__main__":
	#debug
	#current_url = search_baike_item('邢永明(刑永明)')#金素妍(1980年出生韩国女演员)
	#html_content = clean_html(current_url)
	fw = codecs.open('D:\\xxx0624\\insuranceQA\\corpus\\nlpcc16-data\\ENTITY_SET\\celebrity.Detail.ENTITYSET.txt', 'a+', encoding='utf-8-sig')
	with codecs.open('D:\\xxx0624\\insuranceQA\\corpus\\nlpcc16-data\\ENTITY_SET\\celebrity.ENTITYSET.txt', encoding='utf-8-sig') as f:
		line_list = []
		for line in f:
			line = line.strip()
			if line != '':
				line_list.append(line)
		err_count = 0
		index = 0
		while index < len(line_list):
			if index < 17850:
				index += 1
				continue
			line = line_list[index]
			print '\n[', index, ']', line.strip()
			line = line.strip()
			if line == '':
				continue
			#print chardet.detect('戴恩')
			print chardet.detect(line.encode('utf-8'))
			current_url = search_baike_item(line)
			if current_url == -1:
				err_count += 1
				fw.write(line + '\n')
			else:
				print current_url
				html_content = clean_html(current_url)
				if html_content is None:
					print index, '[', err_count, ']clean error...we will search again...'
					#fw.write(line + '\n')
					continue
				fw.write(line + ' ' + html_content + '\n')
			index += 1
		print 'error count =', err_count
		fw.close()
