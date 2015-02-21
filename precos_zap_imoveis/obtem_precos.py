# -*- encoding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodecsv, time

state = "rio de janeiro"
# cities = ["tangua"]
cities = ["belford roxo",
		"cachoeiras de macacu",
		"duque de caxias",
		"guapimirim",
		"itaborai",
		"itaguai",
		"japeri",
		"mage",
		"mangaratiba",
		"marica",
		"mesquita",
		"nilopolis",
		"niteroi",
		"nova iguacu",
		"paracambi",
		"queimados",
		"rio bonito",
		"rio de janeiro",
		"sao goncalo",
		"sao joao de meriti",
		"seropedica",
		"tangua"]

driver = webdriver.Firefox()
wait_time = 20
driver.implicitly_wait(20) # seconds

url = "http://www.zap.com.br/imoveis/fipe-zap-b/"
driver.get(url)

result_list = []
csv_header = ["Tipo de Imovel","Cidade","Bairro","Metro Quadrado","Amostra"]
with open('resuts.csv', 'wb') as f:
	c = unicodecsv.DictWriter(f,csv_header, delimiter=";", encoding="utf-8")
	c.writeheader()

	# Seleciona Tipos de imovel
	home_type_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ucEstatisticas_drpTipoImovelPreco")
	for home_type_option in home_type_element.find_elements_by_tag_name("option"):
		home_type = home_type_option.get_attribute("value")
		print "Imovel do Tipo: %s" % home_type
		home_type_option.click()

		# Seleciona Estado:
		state_xpath = "//select[@name='ctl00$ContentPlaceHolder1$ucEstatisticas$drpEstadoPreco']/option[@value='%s']" % state
		driver.find_element_by_xpath(state_xpath).click()

		# Seleciona Cidade:
		city_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ucEstatisticas_drpCidadePreco")
		for city_option in city_element.find_elements_by_tag_name("option"):
			city = city_option.get_attribute("value")
			if city in cities:
				print "--->Cidade: %s..." % city
				city_option.click()

				time.sleep(1)
				while len(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ucEstatisticas_drpBairro1Preco").find_elements_by_tag_name("option")) <= 1:
					time.sleep(1)

				# Seleciona Bairros:
				neighborhood_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ucEstatisticas_drpBairro1Preco")
				for neighborhood_option in neighborhood_element.find_elements_by_tag_name("option"):
					neighborhood = neighborhood_option.get_attribute("value")
					if neighborhood != "":
						print "------>Bairro: %s..." % neighborhood
						neighborhood_option.click()

						# Obtém Preço:
						result = {}
						result["Tipo de Imovel"] = home_type
						result["Cidade"] = city
						result["Bairro"] = neighborhood

						elem_found = False
						while not elem_found:
							try:
								result["Metro Quadrado"] = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ucEstatisticas_tblEstatisticas"]/tbody/tr[2]/td[2]').text.replace("R$ ","").replace(".","")
								result["Amostra"] = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ucEstatisticas_tblEstatisticas"]/tbody/tr[2]/td[3]').text
								elem_found = True
							except:
								print "waiting to try again..."
								time.sleep(2)

						print result
						c.writerow(result)
						result_list.append(result)
	f.close()
driver.close()