from tkinter import W
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import uuid
import os
import json
from pathlib import Path


class Scraper():

    def __init__(self) -> None:
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options = Options() 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless") 
        options.add_argument("window-size=1920,1080") 
        options.add_argument("--start-maximized")
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(options=options)
        URL = 'https://www.asos.com/men/new-in/new-in-clothing/cat/?cid=6993&nlid=mw|clothing|shop+by+product|new+in'
        self.driver.get(URL)
        time.sleep(3)

        

    def __cookies(self) -> webdriver.Chrome:
        #page_source = self.driver.page_source
        #with open ("/data_collection/images/html.txt", "w") as outfile:
            #outfile.write(page_source)
            #print(page_source)
        try:
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
            accept_cookies_button.click()
            time.sleep(1)
        except AttributeError: # If you have the latest version of selenium, the code above won't run because the "switch_to_frame" is deprecated
            self.driver.get_screenshot_as_file("/data_collection/images/test1.png")
            #self.driver.save_screenshot('scraper_test.png')
            self.driver.switch_to.frame('onetrust-consent-sdk') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
            accept_cookies_button.click()
            time.sleep(1)

        except:
            pass

    def __get_links(self) ->list:
        self.__cookies()
        #self.driver.get_screenshot_as_file("screenshot.png")
        clothes_container = self.driver.find_element(by=By.XPATH, value='//*[@class="RIQzlgo"]')
        clothes_list = clothes_container.find_elements(by=By.XPATH, value='./article')
        link_list = []

        for clothes in clothes_list:
            a_tag = clothes.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
            
        print(f'There are {len(link_list)} items of clothing in this page')
        return link_list

    def __create_id(self):
        id = str(uuid.uuid4())
        
        return id

    def __create_dict(self, id, description, price, colour):
        id_dict = {}

        id_dict['id'] = id
        id_dict['description'] = description
        id_dict['price'] = price
        id_dict["colour"] = colour
        return id_dict

    def __get_data(self):
        clothes = []
        clothes.extend(self.__get_links())

        clothes_list = []

        try:

            for links in clothes:
                self.driver.get(links)
                description = self.driver.find_element(by=By.TAG_NAME, value='h1').text
                price = self.driver.find_element(by=By.XPATH, value='//span[@data-test-id="current-price"]').text
                colour = self.driver.find_element(by=By.XPATH, value='//span[@class="product-colour"]').text
                id = self.__create_id()
                product_dict = self.__create_dict(id, description, price, colour)
                clothes_list.append(product_dict)

        except NoSuchElementException:
            pass
        
        return clothes_list



    def create_file(self):
        directory = 'raw_data'
        parent_dir = '/Users/wadirmalik/Desktop/Data_Collection_Pipeline'
        directory2 = 'Asos'

        asos_path = os.path.join(parent_dir, directory, directory2)

        Path(asos_path).mkdir(parents=True, exist_ok=True) 

        #os.mkdir(asos_path)

        return asos_path

    def save_to_file(self, path, product_dict_list):    
        with open(path + "/id_dict.json", "w") as outfile:
            json.dump(product_dict_list, outfile)

    def run_scraper(self):
        self.__cookies()
        self.__get_links()
        self.__create_id()
        available_clothes_list = self.__get_data()
        available_path = self.create_file()

        return available_path, available_clothes_list
