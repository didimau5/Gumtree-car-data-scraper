import csv
import time

from bs4 import BeautifulSoup
from nordvpn_switcher import initialize_VPN, rotate_VPN
from numpy import random
import os
from webdriver_manager.chrome import ChromeDriverManager
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth



options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome("C:\SeleniumDrivers\chromedriver.exe", options=options)

url_page = "https://www.gumtree.com/cars/uk"  #

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


def get_urls(url):
    hrefs = []
    driver.get(url)
    car_maxi_blades = driver.find_elements(By.CLASS_NAME, 'listing-maxi')
    for i in car_maxi_blades:
        soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
        for ele in soup.findAll('a', {'class': 'listing-link'}):
            listing = "https://www.gumtree.com" + ele['href']
            hrefs.append(listing)

    return hrefs


def next_page(page):
    return "https://www.gumtree.com/cars/uk/page" + str(page)


get_urls(url_page)


def write_data(car_values):
    with open('GumtreeData.csv', 'a', encoding='UTF8', newline='\n') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(car_values)


def getData(urlD):
    driver.get(urlD)
    r = s.get(urlD)
    driver.implicitly_wait(5)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Click on Cookie buuton
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except:
        pass
    # Get all tabs element
    parentList = driver.find_elements(By.XPATH, "//h4[@data-q='motors-attributes-titles']")
    price = soup.find('h3', {'class': 'css-sik94l e1pt9h6u2'})
    name = soup.find( 'h1', {'class': 'css-4rz76v e1pt9h6u6'})
    car = [price.text, name.text]
    seen = set(car)
    for e in parentList[:3]:
        driver.execute_script("arguments[0].click();", e)
        driver.implicitly_wait(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        data = soup.find_all('ul', {'class': 'css-kcx0xb e14ksbtl6'})
        for a in data:
            car.append("SEPARATOR")
            for i in a:
                if i.text not in seen:
                    seen.add(i.text)
                    car.append(i.text)

    number_of_variables = len(parentList) - 3

    for e in parentList[-number_of_variables:]:
        driver.execute_script("arguments[0].click();", e)
        driver.implicitly_wait(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        data2 = soup.find_all('ul', {'class': 'css-16685j5 e14ksbtl6'})
        for a in data2:
            car.append("SEPARATOR")
            for i in a:
                if i.text not in seen:
                    seen.add(i.text)
                    car.append(i.text)

    print(car)
    return car


initialize_VPN(save=1, area_input=['complete rotation'])
counter = 1
driver.get(url_page)
for i in range(7443):
    rotate_VPN()
    driver.get(next_page(counter))
    s = HTMLSession()
    list_of_url = get_urls(url_page)  #
    print("getting list of url")
    for url in list_of_url:
        try:
            write_data(getData(url))
        except:
            pass
            print("That one got away")
    ulr_page = next_page(counter)
    counter += 1
    print("Page " + str(counter))
    driver.get(url_page)


# car = getData("https://www.gumtree.com/p/nissan/2017-nissan-juke-1.5-dci-tekna-pulse-euro-6-s-s-5dr-hatchback-diesel-manual/1437058688")
# write_data(car)
