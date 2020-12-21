#system libraries
import os
import random
import time
from dotenv import load_dotenv

load_dotenv()

#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

email = os.getenv('email')
pw = os.getenv('pw')
reservation_date = '12-28-2020'
reservation_times = ['1:00pm', '10:30am', '11:00am', '11:20am', '11:15am']
# num_guests = 2

def delay ():
    time.sleep(random.randint(2,3))

def solve_audio_challenge (driver):
	# click on the play button
	driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

	# get the mp3 audio file
	src = driver.find_element_by_id("audio-source").get_attribute("src")
	print("[INFO] Audio src: %s"%src)

	#download the mp3 audio file from the source
	urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
	sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
	sound.export(os.getcwd()+"\\sample.wav", format="wav")
	sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
	r = sr.Recognizer()

	with sample_audio as source:
	    audio = r.record(source)

	#translate audio to text with google voice recognition
	key = r.recognize_google(audio)
	print("[INFO] Recaptcha Passcode: %s"%key)

	#key in results and submit
	driver.find_element_by_id("audio-response").send_keys(key.lower())
	driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)

def solve_captcha (driver):
	delay()
	# switch to recaptcha audio control frame
	driver.switch_to.default_content()

	frames = []
	for i in range(5, 8):
		element_is_present = len(driver.find_elements_by_xpath("/html/body/div[" + str(i) + "]/div[2]")) > 0
		if element_is_present:
			html_body = driver.find_element_by_xpath("/html/body/div[" + str(i) + "]/div[2]")
			frames = html_body.find_elements_by_css_selector("iframe")
			if len(frames) > 0:
				print("/html/body/div[" + str(i) + "]" + html_body.get_attribute('innerHTML'))
				break

	driver.switch_to.frame(frames[0])
	delay()

	# click on audio challenge
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()
	driver.find_element_by_id("recaptcha-audio-button").click()

	# switch to recaptcha audio challenge frame
	driver.switch_to.default_content()
	frames = driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(frames[-1])
	delay()

	solve_audio_challenge(driver)
	delay()
	# Check if multiple attempts required
	# repeat_verify_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Multiple correct solutions required')]")))
	repeat_verification_required = len(driver.find_elements_by_xpath("//*[contains(text(), 'Multiple correct solutions required')]")) > 0
	attempt = 1
	while (repeat_verification_required):
		print('attempt number: ' + str(attempt))
		attempt += 1
		solve_audio_challenge(driver)
		delay()
		repeat_verification_required = len(driver.find_elements_by_xpath("//*[contains(text(), 'Multiple correct solutions required')]")) > 0
		print('repeat_verification_required: ' + str(repeat_verification_required))


	driver.switch_to.default_content()
	delay()
	# driver.find_element_by_id("recaptcha-demo-submit").click()
	# delay()


def make_reservation ():
	# Initiate the browser
	browser = webdriver.Chrome(ChromeDriverManager().install())

	delay()
	# Open the website
	browser.get('https://foreupsoftware.com/index.php/booking/20330/4502#/teetimes')

	# Login to the site
	browser.find_element_by_class_name('login').click()
	browser.find_element_by_name('email').send_keys(email)
	browser.find_element_by_name('password').send_keys(pw)
	browser.find_element_by_xpath('//*[@id="login"]/div/div[3]/div[1]/button[1]').click();

	reserve_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Reserve a time now.')]")))
	reserve_button.click()
	# delay()

	# Reserve appointment
	WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/button"))).click()
	# browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button").click()
	date_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "date")))
	for x in '12-16-2020':
	    date_field.send_keys(Keys.BACK_SPACE);
	date_field.send_keys(reservation_date)
	date_field.send_keys(Keys.ENTER)

	# Pick time slot
	for reservation_time in reservation_times:
		print('reservation_time: ' + reservation_time)
		time_slots = browser.find_elements_by_xpath("//*[contains(text(), '" + reservation_time + "')]")
		if len(time_slots) > 0:
			time_slots[0].click()
			break

	book_time = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Book Time')]")))
	book_time.click()

	# Solve CAPTCHA
	solve_captcha(browser)
	print('hello')

	# Add guests
	# guest_buttons = driver.find_elements_by_xpath("//button[contains(text(), 'Guest')]")
	# print('guest buttons length: ' + len(guest_buttons))
	# for i in num_guests:
	# 	guest_buttons[i].click()

	# Click Continue
	continue_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Continue')]")))
	continue_button.click()

	# Click Book Time
	book_time = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Book Time')]")))
	book_time.click()


reservation = make_reservation()

# https://medium.com/analytics-vidhya/how-to-easily-bypass-recaptchav2-with-selenium-7f7a9a44fa9e
# https://ohyicong.medium.com/how-to-bypass-recaptcha-with-python-1d77a87a00d7