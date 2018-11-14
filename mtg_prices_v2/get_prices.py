# -*- encoding:utf-8 -*-
import spreadsheet
from scrappers import *
from collections import OrderedDict

def get_prices():
	# Spreadsheet Data:
	WORKBOOK_NAME = 'MTG'
	INPUT_WORKSHEET_NAME = 'Cards Input'
	OUTPUT_WORKSHEET_NAME = 'Cards Output'
	MAX_STORES = 10

	# Get Cards From Spreadsheet
	print('Getting cards from spreadsheet...')
	workbook = spreadsheet.open(WORKBOOK_NAME)
	input_worksheet = workbook.worksheet(INPUT_WORKSHEET_NAME)
	cards = input_worksheet.get_all_records()

	# Scrappers Initiation:
	print('Initiating scrappers...')
	scrappers = []
	scrappers.append(LigaMagicScrapper())

	# Get Results From scrappers
	print('Scrapping cards info...')
	result = OrderedDict()
	for card in cards:
		card_name = card["Name"]
		for scrapper in scrappers:
			scrapper_results = scrapper.get_price(card_name)
			for store_name in scrapper_results:
				card_dict = {card_name:scrapper_results[store_name]}
				if store_name not in result:
					result.update({store_name:card_dict})
				else:
					result[store_name].update(card_dict)

	print('Finishing scrappers...')
	for scrapper in scrappers:
		scrapper.close_connection()

	# Clear or create output spreadsheet:
	print('Clearing output sheet...')
	output_worksheet = None
	try:
		output_worksheet = workbook.worksheet(OUTPUT_WORKSHEET_NAME)
		output_worksheet.clear()
		output_worksheet.resize(len(cards)+3, min(MAX_STORES,len(result))+2)
	except:
		output_worksheet = workbook.add_worksheet(OUTPUT_WORKSHEET_NAME, len(cards)+3, min(MAX_STORES,len(result))+2)
	spreadsheet.update_cell(output_worksheet,1,1,'Name')
	spreadsheet.update_cell(output_worksheet,1,2,'Quantity')
	spreadsheet.update_cell(output_worksheet,2,1,'# Cards Found')
	spreadsheet.update_cell(output_worksheet,3,1,'R$ Total')

	print('Filling output sheet...')
	# Filling the first/second column
	ordered_cards = OrderedDict()
	row = 4
	columns = 2
	for card in cards:
		ordered_cards[card['Name']] = card['Quantity']
		spreadsheet.update_cell(output_worksheet,row,1,card['Name'])
		spreadsheet.update_cell(output_worksheet,row,2,card['Quantity'])
		row += 1

	# Sorting Result:
	for store_name in result:
		total_value = 0
		for card_name in result[store_name]:
			total_value += result[store_name][card_name]*ordered_cards[card_name]
		result[store_name]['# Cards Found'] = len(result[store_name])
		result[store_name]['R$ Total'] = total_value
	result = OrderedDict(sorted(result.items(),key=lambda item: (-item[1]['# Cards Found'],item[1]['R$ Total'])))

	# Filling with data:
	stores_count = 0
	for store_name in result:
		stores_count += 1
		if stores_count <= MAX_STORES:
			# Get store column number
			column_number = None
			total_value = 0
			try:
				column_number = output_worksheet.find(store_name)._col
			except:
				columns += 1
				column_number = columns
				spreadsheet.update_cell(output_worksheet,1,column_number,store_name)
			# Fill card prices:
			for card_name in result[store_name]:
				card_price = result[store_name][card_name]
				row_number = output_worksheet.find(card_name)._row
				spreadsheet.update_cell(output_worksheet,row_number,column_number,result[store_name][card_name])
	
	print('Done! Check https://docs.google.com/spreadsheets/d/1veuor_lsPmqPMHhUN_78eV6vuSRKemdalbLMfICun2g/edit#gid=965121549 for results!')
