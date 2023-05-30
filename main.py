from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import concurrent.futures
import requests
import os
import sys
from urllib.parse import urlparse

options = Options()
options.add_argument('--headless')
formats = ['png', 'jpg']


def createFolders():
    for i in formats:
        if not os.path.exists(i):
            os.makedirs(i)


def cleanFolders():
    for i in formats:
        for nomeArquivo in os.listdir(i):
            caminho = os.path.join(i, nomeArquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)


def downloadImages(site):
    print('searching', site)
    driver = webdriver.Chrome('path/to/chromedriver', options=options)

    driver.get(site)

    images = driver.find_elements(By.TAG_NAME, 'img')

    print(site, ' - ', len(images), 'images')
    for image in images:
        image_url = image.get_attribute('src')
        filename = os.path.basename(urlparse(image_url).path)
        quantFormats = len(formats)
        for i in formats:
            if image_url.endswith('.'+i):
                response = requests.get(image_url)
                with open('./'+i+'/'+filename, 'wb') as file:
                    file.write(response.content)
            else:
                quantFormats -= 1
        if quantFormats == 0:
            print(image_url, 'not scraped')
    driver.quit()


createFolders()
cleanFolders()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1]) as file:
                for line in file:
                    site = line.strip()
                    print(site)
                    executor.submit(downloadImages, site)
        else:
            executor.submit(downloadImages, sys.argv[1])
    else:
        print('No website or file .txt selected for scraping')
