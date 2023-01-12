from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException

driver = webdriver.Chrome("./chromedriver2")
driver.get("https://www.kamis.or.kr/customer/main/main.do")
print(driver)