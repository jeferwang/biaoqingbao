# coding=utf-8
# 闲来无聊练练手
import urllib2
import codecs
import re
import os
import time
from bs4 import BeautifulSoup


class BiaoQingBao(object):
	def __init__(self, first_page, page_num):
		self.first_page = first_page
		self.page_num = page_num
		self.url_list = []
		for i in range(self.first_page, self.first_page + self.page_num):
			self.url_list.append('http://www.doutula.com/article/list/?page=%d' % i)
		print(self.url_list)
	
	def craw(self, url):
		html_source = urllib2.urlopen(url).read()
		father_page_bsobj = BeautifulSoup(html_source, 'lxml')
		find_all_child = father_page_bsobj.find_all("a", {"class": "list-group-item"})
		for ch_li in find_all_child:
			try:
				child_page_source = urllib2.urlopen(ch_li['href']).read()
			except:
				continue
			child_page_bsobj = BeautifulSoup(child_page_source, 'lxml')
			group_name = child_page_bsobj.find("h3").get_text().strip()
			print(group_name)
			images = child_page_bsobj.find_all("img")
			for img in images:
				if img['src'].find('large') != -1:
					print(img['src'])
					self.img_downloader(group_name, img['src'])
	
	def img_downloader(self, group, src):
		group = re.subn(r'[<>/|:"\'*?]', '_', group)[0]
		file_path = "./biaoqingbao/" + group
		try:
			os.makedirs(file_path)
		except:
			pass
		finally:
			img_name = src.split('/')[-1]
			try:
				open(file_path + '/' + img_name, 'r')
			except IOError:
				try:
					web_img = urllib2.urlopen(src, timeout=10).read()
					down_file = open(file_path + '/' + img_name, 'wb')
					down_file.write(web_img)
					down_file.close()
				except:
					pass


if __name__ == '__main__':
	first = int(input("请输入初始页码：\n"))
	num = int(input("请输入页码数，不大于444：\n"))
	craw = BiaoQingBao(first, num)
	count_page = len(craw.url_list)
	for page_n in range(0, count_page):
		current_url = craw.url_list.pop(0)
		craw.craw(current_url)
