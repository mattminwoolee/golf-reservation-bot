import os
import random
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

email = 'mattminwoolee@gmail.com'
pw = ''

def delay ():
    time.sleep(random.randint(2,3))

def solve_captcha (driver):
	#switch to recaptcha frame
	frames=driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(frames[0]);
	delay()
	#click on checkbox to activate recaptcha
	driver.find_element_by_class_name("recaptcha-checkbox-border").click()
	#switch to recaptcha audio control frame
	driver.switch_to.default_content()
	frames=driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
	driver.switch_to.frame(frames[0])
	delay()
	#click on audio challenge
	driver.find_element_by_id("recaptcha-audio-button").click()
	#switch to recaptcha audio challenge frame
	driver.switch_to.default_content()
	frames= driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(frames[-1])
	delay()
	#click on the play button
	driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()


try:
	# Initiate the browser
	browser = webdriver.Chrome(ChromeDriverManager().install())

	delay()
	# Open the website
	browser.get('https://foreupsoftware.com/index.php/booking/20330/4502#/teetimes')

	# # Login to the site
	browser.find_element_by_class_name('login').click()
	browser.find_element_by_name('email').send_keys(email)
	browser.find_element_by_name('password').send_keys(pw)
	browser.find_element_by_xpath('//*[@id="login"]/div/div[3]/div[1]/button[1]').click();


	reserve_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Reserve a time now.')]")))
	reserve_button.click()

	# Reserve appointment
	browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button").click()
	date = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "date")))
	for x in '12-16-2020':
	    date.send_keys(Keys.BACK_SPACE);
	date.send_keys('12-19-2020')
	date.send_keys(Keys.ENTER)
	reservation_slot = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '4:00pm')]")))
	reservation_slot.click()
	

	book_time = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '4:00pm')]")))
	book_time.click()


	frames=driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(frames[0]);
	delay()
except:
    print("[-] ERROR")

# https://medium.com/analytics-vidhya/how-to-easily-bypass-recaptchav2-with-selenium-7f7a9a44fa9e
# https://ohyicong.medium.com/how-to-bypass-recaptcha-with-python-1d77a87a00d7