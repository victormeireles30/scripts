# -*- encoding:utf-8 -*-
from mtg_scrappers import *
import sys, json
import unicodecsv

def main(argv):
	cards = []
	with open('cards.csv', 'rb') as csvfile:
		reader = unicodecsv.DictReader(csvfile, fieldnames=['Nome', 'Qtd'], delimiter=';')
		# skip headers:
		reader.next()
		for row in reader:
			cards.append(row)

	store_list = []
	store_list.append(ChqScrapper())
	store_list.append(DomainScrapper())
	store_list.append(AcademiaScrapper())
	store_list.append(KinoScrapper())
	store_list.append(LigaMagicScrapper())

	for card in cards:
		for store in store_list:
			store_result = store.get_price(card["Nome"])
			card[store.name] = store_result["price"]

	csv_header = ["Nome","Qtd"]
	for store in store_list:
		csv_header.append(store.name)
		store.close_connection()
	with open('resuts.csv', 'wb') as f:
		c = unicodecsv.DictWriter(f,csv_header, delimiter=";", encoding="utf-8")
		c.writeheader()
		c.writerows(cards)
		f.close()

if __name__ == '__main__':
	main(sys.argv)