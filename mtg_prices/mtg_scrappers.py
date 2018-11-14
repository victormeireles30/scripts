# -*- encoding:utf-8 -*-
import sys, re, json
from mechanize import Browser, HTTPError, URLError
from mechanize._mechanize import LinkNotFoundError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib

class MechanizeStoreScrapper(object):
	def __init__(self):
		self.browser = Browser()
		self.browser.set_handle_robots(False)
		self.browser.set_handle_equiv(False)
		self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	def get_price(self,card):
		print("Obtendo dados de '%s' em %s..." % (card, self.name))
		url = self.url_base + urllib.urlencode({self.url_filter : card})
		return self.find_price(card,url)

	def close_connection(self):
		pass

class AcademiaScrapper(MechanizeStoreScrapper):
	def __init__(self):
		self.name = "Academia"
		self.url_base = "http://www.academiadejogos.com.br/index.php?route=product/search&"
		self.url_filter = "filter_name"
		super(AcademiaScrapper, self).__init__()

	def find_price(self,card,url):
		self.browser.open(url)
		soup = BeautifulSoup(self.browser.response().read())
		
		price = None
		for product in soup.find(attrs={'class':'product-list'}).find_all(attrs={'class':'price'}):
			if 'Estoque:' in product.text:
				next_price = float(re.search("[R][$][0-9]+[,][0-9]+",product.text).group(0).replace("R$","").replace(",","."))
				if not price or price > next_price:
					price = next_price

		return {"price":price}

class LigaMagicScrapper(MechanizeStoreScrapper):
	def __init__(self):
		self.name = "LigaMagic"
		self.url_base = "http://www.ligamagic.com.br/?view=cartas/card&"
		self.url_filter = "card"
		super(LigaMagicScrapper, self).__init__()

	def find_price(self,card,url):
		self.browser.open(url)
		soup = BeautifulSoup(self.browser.response().read())
		
		price = re.search('[0-9]+[,][0-9]+',soup.find(attrs={'class':'hmin44 preMed brdb'}).text).group(0).replace(',','.')

		return {"price":price}

class KinoScrapper(MechanizeStoreScrapper):
	def __init__(self):
		self.name = "Kino"
		self.url_base = "http://www.kinoenecards.com.br/?view=item&"
		self.url_filter = "item"
		super(KinoScrapper, self).__init__()

	def find_price(self,card,url):
		self.browser.open(url)
		soup = BeautifulSoup(self.browser.response().read())
		
		price = None
		for item_price in soup.find_all(attrs={"class":"colLine bgGray tPP"}):
			if "Sem estoque" not in item_price.parent.text:
				next_price = re.search("[0-9]+[,]+[0-9]+",item_price.text).group(0).replace(",",".")
				if not price or price > next_price:
					price = next_price

		return {"price":price}

class SeleniumStoreScrapper(object):
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.wait_time = 20
		self.driver.implicitly_wait(20) # seconds
		
	def get_price(self,card):
		print("Obtendo dados de '%s' em %s..." % (card, self.name))
		url = self.url_base + urllib.urlencode({self.url_filter : card})
		return self.find_price(card,url)

	def close_connection(self):
		self.driver.close()

class DomainScrapper(SeleniumStoreScrapper):
	def __init__(self):
		self.name = "Domain"
		self.url_base = "http://www.domaingames.com.br/Busca_Avancada.asp?"
		self.url_filter = "q"
		super(DomainScrapper, self).__init__()

	def find_price(self,card,url):
		self.driver.get(url)
		
		price = None
		for product in self.driver.find_element_by_id("ListadeProdutosAvancada").find_elements_by_tag_name("li"):
			if product.find_element_by_class_name("ingles").text == card:
				if "R$" in product.find_element_by_class_name("vista").text:
					next_price = float(product.find_element_by_class_name("vista").text.replace("R$","").replace(",",".").replace(" ",""))
					if not price or price > next_price:
						price = next_price

		return {"price":price}

class ChqScrapper(SeleniumStoreScrapper):
	def __init__(self):
		self.name = "Chq"
		self.url_base = "http://loja.chq.com.br/Busca.aspx?"
		self.url_filter = "strBusca"
		super(ChqScrapper, self).__init__()

	def find_price(self,card,url):
		self.driver.get(url)
		
		price = None
		products = self.driver.find_elements_by_class_name('PrecoProduto')
		if products:
			for product in products:
				next_price = float(product.text.replace("R$","").replace(",",".").replace(" ",""))
				if not price or price > next_price:
					price = next_price

		return {"price":price}