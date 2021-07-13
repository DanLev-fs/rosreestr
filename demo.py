import webbrowser,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import requests
from time import sleep
from captcha_solver import CaptchaSolver
from PIL import Image
from io import BytesIO

api = "" #Ключ антикапчи
key = "" #Ключ ЕГРН
kadastr = "" #Кадастровый номер
region = "Тверская область" #Регион
headers = {"Host": "rosreestr.gov.ru",
"Connection": "keep-alive",
"sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
"sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
"Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "no-cors",
"Sec-Fetch-Dest": "image",
"Referer": "https://rosreestr.gov.ru/wps/PA_AIRGKN/VAADIN/themes/reindeer/styles.css",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6,bg;q=0.5,th;q=0.4,ja;q=0.3,fr;q=0.2,tr;q=0.1"}

def captcha_solve(url, key):
	if key is not None:
		try:
			solver = CaptchaSolver('antigate', api_key=key)
			raw_data = open('captha.png', 'rb').read()
			key = solver.solve_captcha(raw_data)
			return key
		except Exception as e:
			print("Exception: ", e)
	return None
# 
def send_req(browser, apic, keyc):	
	browser.implicitly_wait(40)
	browser.get ('https://rosreestr.ru/wps/portal/p/cc_present/ir_egrn')
	cs = browser.find_elements_by_class_name('v-textfield')
	keyc = keyc.split("-")
	i = 0
	while i != 5:
		cs[i].send_keys(keyc[i])
		sleep(0.2)
		i+=1
	browser.find_element_by_class_name('v-button-caption').click()
	sleep(5)
	cs = browser.find_elements_by_class_name('v-button-caption')
	for i in cs:
		if i.text == "Поиск объектов недвижимости":
			i.click()
			break
	sleep(0.1)
	browser.find_element_by_css_selector('.v-textfield').send_keys(kadastr)
	sleep(0.1)
	cs = browser.find_element_by_class_name('v-filterselect-input')
	cs.click()
	for i in region:
		cs.send_keys(i)
	sleep(1)
	cs.send_keys(Keys.TAB)
	sleep(5)
	for i in browser.find_elements_by_class_name('v-button-caption'):
		if i.text == "Найти":
			i.click()
			break
	sleep(5)
	browser.find_element_by_css_selector(".v-table-table").click()
	sleep(2)
	body = browser.find_element_by_css_selector('body')
	body.send_keys(Keys.PAGE_DOWN)
	body.send_keys(Keys.PAGE_DOWN)
	body.send_keys(Keys.PAGE_DOWN)
	body.send_keys(Keys.PAGE_DOWN)
	sleep(0.5)
	src = browser.find_elements_by_css_selector(".v-embedded.v-embedded-image")[1].find_element_by_tag_name("img").screenshot("captha.png")
	ca = captcha_solve(src, apic)
	
	print(ca)
	sleep(0.5)
	cs = browser.find_element_by_css_selector(".v-textfield")
	cs.click()
	for i in ca:
		cs.send_keys(i)
	for i in browser.find_elements_by_class_name('v-button-caption'):
		if i.text == "Отправить запрос":
			i.click()
			break
	sleep(5)
	
# 
def main():
	browser = webdriver.Chrome()
	send_req(browser, api, key)

main()
