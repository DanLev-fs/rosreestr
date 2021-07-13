from selenium import webdriver
from time import sleep
from captcha_solver import CaptchaSolver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re 
from PIL import Image
import db

url = "https://rosreestr.gov.ru/wps/portal/p/cc_ib_portal_services/online_request"
sub = "Москва"
street_type = "Шоссе"
street = "Ленинградское"
house = "25"
korp = "2"
structure = ""
api = ""

def captcha_solve(key):
	if key is not None:
		try:
			solver = CaptchaSolver('antigate', api_key=key)
			raw_data = open('captha.png', 'rb').read()
			key = solver.solve_captcha(raw_data)
			return key
		except Exception as e:
			print("Exception: ", e)
	return None

def codastrGet(driver, api):
	driver.get(url)
	driver.find_element_by_id("adress").click()
	driver.find_element_by_xpath("//select[@name='subject_id']/option[text()='"+sub+"']").click()
	sleep(0.1)
	driver.find_element_by_xpath("//select[@name='street_type']/option[text()='"+street_type+"']").click()
	sleep(0.1)
	driver.find_element_by_name("street").send_keys(street)
	sleep(0.1)
	driver.find_element_by_name("house").send_keys(house)
	sleep(0.1)
	driver.find_element_by_name("building").send_keys(korp)
	sleep(0.1)
	driver.find_element_by_name("structure").send_keys(structure)
	body = driver.find_element_by_css_selector('body')
	body.send_keys(Keys.PAGE_DOWN)
	sleep(0.2)
	src = driver.find_elements_by_id('captchaImage2')
	elem = ""
	for i in src:
		i.screenshot("captha.png")
		elem = i
	location = elem.location
	size = elem.size
	x = location['x']
	y = location['y']
	width = location['x']+size['width']
	height = location['y']+size['height']
	im = Image.open('captha.png')
	im = im.crop((int(x), int(y), int(width), int(height)))
	im.save('captha.png')
	ca = captcha_solve(api)
	print(ca)
	driver.find_element_by_name("captchaText").send_keys(ca)
	sleep(0.1)
	driver.find_element_by_id("submit-button").click()
	sleep(0.1)
	cout = 0
	while True:
		try:
			j=0
			base = []
			while j!=20:
				nb = ""
				at = ""
				tag = driver.find_element_by_id("js_oTr"+str(j))
				atag = tag.find_element_by_tag_name("a").text.replace("                                    ", '')
				nobrtag = tag.find_elements_by_tag_name("nobr")
				for i in nobrtag:
					if re.search(r'\d{2}[:-]\d{2}[:-]\d{7}', i.text):
						nb = i.text
						break
				base.append((nb, atag))	
				j+=1
			db.addstep1(base)
			next = driver.find_element_by_xpath('//img[@alt="Следующая страница"]')
			if next.get_attribute("src") == "https://rosreestr.gov.ru/wps/PA_RRORSrviceExtended/images/common/controls/arrows_right.gif":
				next.click()
				cout+=1
			else:
				driver.save_screenshot('screen1.png') 
				break
		except NoSuchElementException:
			break
	print("parse page cout: " + str(cout))

def main():
	driver = webdriver.PhantomJS(service_args=[
        '--ignore-ssl-errors=true', 
        '--ssl-protocol=any', 
        '--web-security=false',
    ],
    # and also other capabilities:
    desired_capabilities={
        'phantomjs.page.settings.resourceTimeout': '5000',
        'phantomjs.page.settings.userAgent': (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )
    }) # or add to your PATH
	driver.set_window_size(1024, 768) # optional
	codastrGet(driver, api)
	db.getallstep1()

main()
