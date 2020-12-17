from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

email = 'mattminwoolee@gmail.com'
pw = 'Losverdesthensleep22'

# Initiate the browser
browser = webdriver.Chrome(ChromeDriverManager().install())

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