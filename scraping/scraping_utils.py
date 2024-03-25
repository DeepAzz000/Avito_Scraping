import logging
from logging.config import dictConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime


def navigate_to_website(page_number):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        website = f'https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre?o={page_number}'
        driver.get(website)
        logging.info(f"Navigated to page {page_number}")
        return driver
    except Exception:
        logging.info("Couldn't navigate to main element")

def get_links(driver):
    try:
        path_to_box_of_cars = "//*[@id='__next']/div/main/div/div[5]/div[1]/div/div[1]"
        main_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path_to_box_of_cars)))
        logging.info("Main element found")
        tags = main_element.find_elements(By.TAG_NAME, 'a')
        links = []
        for tag in tags:
            link = tag.get_attribute("href")
            if not link: continue
            links.append(link)
        logging.info("Extracted tags")
        return links
    except Exception:
        logging.info("Could not find main element")

def get_car_characteristics(driver, links):
    logging.info("Getting car elements")
    car_data = []
    for url in links:
        driver.get(url)        
        car_dict = {}
        main_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]')))
        car_dict['Scraping_time'] = get_current_timestamp()
        try:
            car_dict['Name'] = main_info.find_element(By.XPATH, "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/h1").text
            logging.info("Car name found")
        except:
            car_dict['Name'] = 'Not Provided'
            logging.info("Car name not found")
        try:
            car_dict['Prix'] = main_info.find_element(By.XPATH, "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p").text
            logging.info("Car Price found")
        except:
            car_dict['Prix'] = 'Not Provided'
            logging.info("Car price not found")
        try:
            car_dict['Location'] = main_info.find_element(By.XPATH, "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span[1]").text
            logging.info("Car Location found")
        except:
            car_dict['Location'] = 'Not Provided'
            logging.info("Car location not found")
        
        
        data_types = ['Type', 'Secteur', 'Première main', 'Nombre de portes', 'Modèle', 'Kilométrage', 'Marque', 'Année-Modèle', 'État', 'Origine' ]
        li_xpath = "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/ol/li["
        for datatype in data_types:
            for i in range(1, 10):
                try:
                    li_element = main_info.find_element(By.XPATH, str(li_xpath) + str(i) + ']')
                    first_span = li_element.find_element(By.XPATH, ".//span[1]")
                    first_span_text = first_span.text
                    if first_span_text == datatype:
                        second_span = li_element.find_element(By.XPATH, ".//span[2]")
                        second_span_text = second_span.text
                        car_dict[first_span_text] = second_span_text
                        logging.info(f'{str(datatype)} found')
                        break
                    else: 
                        car_dict[datatype] = 'None'
                except Exception:
                    car_dict[datatype] = 'None'
        car_data.append(car_dict)
    logging.info("Cars elements found")        
    return car_data

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def write_to_csv(car_data, csv_file_path):
    
    try:
        car_data_file = open(csv_file_path, mode='a', newline='', encoding='utf-8')
        car_data_writer = csv.DictWriter(car_data_file, fieldnames=car_data[0].keys())
        if car_data_file.tell() == 0:
            car_data_writer.writeheader()
        logging.info(f'Writing to {csv_file_path}')
        for car in car_data:
            car_data_writer.writerow(car)
        logging.info(f'Writing to {csv_file_path} is DONE')
    except Exception as e:
        logging.error(f"Exception occurred while writing to CSV: {e}")
