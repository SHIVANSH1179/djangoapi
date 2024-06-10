# dcoins/tasks.py

import requests
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@shared_task
def get_crypto_data(coin_symbols):
    url = 'https://coinmarketcap.com/'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    data = {}
    
    for symbol in coin_symbols:
        try:
            search_box = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"]')
            search_box.clear()
            search_box.send_keys(symbol)
            
            # Wait for results and fetch the first result
            driver.implicitly_wait(5)
            result = driver.find_element(By.CSS_SELECTOR, 'div.cmc-search-result__result--1').click()
            driver.implicitly_wait(5)
            
            price = driver.find_element(By.CSS_SELECTOR, 'div.priceValue___11gHJ').text
            data[symbol] = {'price': price}
        except Exception as e:
            data[symbol] = {'error': str(e)}
    
    driver.quit()
    return data
