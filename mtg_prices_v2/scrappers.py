# -*- encoding:utf-8 -*-
# import re
# from robobrowser import RoboBrowser
# from bs4 import BeautifulSoup

# print('comecando...')

# # browser = RoboBrowser(user_agent='a python robot',parser='lxml',history=True)
# browser = RoboBrowser(history=True,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101  Firefox/40.1',parser='lxml')
# browser.open('http://www.ligamagic.com.br/?view=cartas/card&card=Martyr+of+Sands')

# # Inspect the browser session
# browser.session.headers['User-Agent']       # a python robot

# print(str(browser.parsed()))

# print('...fim')

from selenium import webdriver
import urllib
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class SeleniumStoreScrapper(object):
	def __init__(self):
		binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
		self.driver = webdriver.Firefox(firefox_binary=binary)
		self.wait_time = 20
		self.driver.implicitly_wait(20) # seconds
		
	def get_price(self,card):
		print("Obtendo dados de '%s' em %s..." % (card, self.name))
		url = self.url_base + urllib.parse.urlencode({self.url_filter : card})
		return self.find_price(card,url)

	def close_connection(self):
		self.driver.close()

class LigaMagicScrapper(SeleniumStoreScrapper):
	def __init__(self):
		self.name = "Liga Magic"
		self.url_base = "http://www.ligamagic.com.br/?view=cartas/card&"
		self.url_filter = "card"
		super(LigaMagicScrapper, self).__init__()

	def find_price(self,card,url):
		self.driver.get(url)
		result = {}
		try:
			for store in self.driver.find_element_by_id("cotacao-1").find_element_by_tag_name('tbody').find_elements_by_tag_name("tr"):
				store_name = store.find_element_by_class_name("banner-loja").find_element_by_tag_name("img").get_attribute('title')
				if "R$" in store.find_element_by_class_name("lj").text:
					store_price = float(store.find_element_by_class_name("lj").text.split('R$ ')[-1].replace(",",".").replace(" ",""))
				result[store_name] = store_price
		except:
			pass
		return result