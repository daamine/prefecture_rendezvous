# Copyright (c) 2021 Amine Daoud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import logging
from pygame import mixer
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Automatic script to notify a RDV in prefecture.')
    parser.add_argument('-u', '--url', default="https://pprdv.interieur.gouv.fr/booking/create/989", required=True, help='url de la page de rendez vous')
    parser.add_argument('-t', '--timeout', default=180, type=int, help='Timeout entre les requetes.')
    return parser.parse_args()

args = parse_args()
URL = args.url
REFRESH_TIMEOUT = args.timeout

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

def refresh(browser):
    if browser.current_url == URL:
        logging.info(f"Refreshing {browser.current_url}")
        browser.refresh()
    else:
        logging.info(f"Reloading URL {URL}")
        browser.get(URL)

def click_button(browser, xpath):
    button = browser.find_element(By.XPATH, xpath)
    button.click()

def check_status(browser):
    list1 = browser.find_elements(By.XPATH, "//*[contains(text(),'" + "pas calendrier disponible" + "')]")
    list2 =  browser.find_elements(By.XPATH, "//*[contains(text(),'" + "surchargé" + "')]")
    list3 =  browser.find_elements(By.XPATH, "//*[contains(text(),'" + "existe plus de plage horaire libre" + "')]")
    for element in list1 + list2 + list3:
        logging.info(f"Status : {element.text}")
    return len(list1) > 0 or len(list2) > 0 or len(list3) > 0

mixer.init()
s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s)
browser.get(URL)

while True:
    try:
        time.sleep(5)
        click_button(browser, "//input[@type='checkbox']")
        time.sleep(5)
        click_button(browser, "//input[@type='submit' and @name='nextButton']")
        time.sleep(10)
        click_button(browser, "//input[@type='radio' and @id='planning990']")
        time.sleep(5)
        click_button(browser, "//input[@type='submit' and @name='nextButton']")
        time.sleep(5)
    except Exception as e:
        logging.error(f"Error occurred when trying to find elements, retrying after 1 minute {e}")
        print(e)
        time.sleep(180)
        refresh(browser)
        continue

    if check_status(browser):
        logging.warning("No appointment found, retrying after 1 minute...")
        time.sleep(REFRESH_TIMEOUT)
        refresh(browser)
    else:
         break

logging.info("Notifying!!!")
alert = mixer.Sound('mixkit-fairy-bells-583.wav')
alert.play(loops=-1)
time.sleep(3600) # sleep one hour
browser.close()