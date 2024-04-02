import logging
from logging.config import dictConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime
import sqlite3
from time import perf_counter

def navigate_to_website(current_page):
    try:
        options = Options()
        options.add_argument('--headless')
        # options.page_load_strategy = 'eager'
        # options.add_argument('--blink-settings=imagesEnabled=false')
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.javascript": 2,
            "profile.default_content_setting_values.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.javascript": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=options)
        website = f'https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre?o={current_page}'
        driver.get(website)
        logging.info(f"Navigated to page {current_page}")
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
    average_time = []
    for url in links:
        start = perf_counter()
        driver.get(url)        
        car_dict = {}
        main_info = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]')))
        car_dict['Scraping time'] = get_current_timestamp()
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
        li_xpath = "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/ol/li"
        try:
            li_elements = main_info.find_elements(By.XPATH, li_xpath)
            for element in li_elements:
                first_span = element.find_element(By.XPATH, ".//span[1]")
                first_span_text = first_span.text
                if first_span.text in ['Type', 'Secteur', 'Première main', 'Nombre de portes', 'Modèle', 'Kilométrage', 'Marque', 'Année-Modèle', 'État', 'Origine']:
                    second_span = element.find_element(By.XPATH, ".//span[2]")
                    second_span_text = second_span.text
                    car_dict[first_span_text] = second_span_text
                    logging.info(f'{str(first_span_text)} found')
                else:
                    car_dict[first_span_text] = "Not Provided"
        except Exception:
            for key in ['Type', 'Secteur', 'Première main', 'Nombre de portes', 'Modèle', 'Kilométrage', 'Marque', 'Année-Modèle', 'État', 'Origine']:
                car_dict[key] = "Not Provided"
        car_data.append(car_dict)
        end = perf_counter()
        average_time.append(end-start)
        logging.info(f" {car_dict['Name']} elements found. Duration: {end-start} ")
    logging.info("Cars elements found")
    avg = sum(average_time)/len(average_time)
    logging.info(f"Average duration time {avg}")
    return car_data

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# def write_to_csv(car_data, output_file_path):
    
    try:
        logging.info(f'Writing to csv file: {output_file_path} started')
        car_data_file = open(output_file_path, mode='a', newline='', encoding='utf-8')
        car_data_writer = csv.DictWriter(car_data_file, fieldnames=car_data[0].keys())
        if car_data_file.tell() == 0:
            car_data_writer.writeheader()
        logging.info(f'Writing to {output_file_path}')
        for car in car_data:
            car_data_writer.writerow(car)
        logging.info(f'Writing to csv file: {output_file_path} is DONE')
    except Exception as e:
        logging.error(f"Exception occurred while writing to CSV: {e}")

def write_to_csv(car_data, output_file_path):
    try:
        logging.info(f'Writing to csv file: {output_file_path} started')
        fieldnames = ['Scraping time', 'Name', 'Prix', 'Location', 'Type', 'Secteur', 'Première main', 'Nombre de portes', 'Modèle', 'Kilométrage', 'Marque', 'Année-Modèle', 'État', 'Origine']
        car_data_file = open(output_file_path, mode='a', newline='', encoding='utf-8')
        car_data_writer = csv.DictWriter(car_data_file, fieldnames=fieldnames)
        if car_data_file.tell() == 0:
            car_data_writer.writeheader()
        logging.info(f'Writing to {output_file_path}')
        for car in car_data:
            row_data = {field: car.get(field, '') for field in fieldnames}
            car_data_writer.writerow(row_data)
        logging.info(f'Writing to csv file: {output_file_path} is DONE')
    except Exception as e:
        logging.error(f"Exception occurred while writing to CSV: {e}")

def write_to_db(car_data):
    try:
        
        logging.info('Writing to SQLite database: "avito_cars.db" started')
        conn = sqlite3.connect("C:\Users\Public\Avito_Scraping.worktrees\v2\output_files\\avito_raw_data.db")
        cur = conn.cursor()
        fieldnames = ['Scraping time', 'Name', 'Prix', 'Location', 'Type', 'Secteur', 'Première main', 'Nombre de portes', 'Modèle', 'Kilométrage', 'Marque', 'Année-Modèle', 'État', 'Origine']
        for car in car_data:
            list_of_tuples = [tuple(car.get(field, '') for field in fieldnames)]
            values = ', '.join(map(str, list_of_tuples))
        cur.execute(f"INSERT INTO cars_data ('Scraping time', 'Name', 'Prix', 'Location', 'Type', 'Secteur', 'Première main', 'Nombre de portes', 'Modèle', 'Kilométrage', 'Marque', 'Année-Modèle', 'État', 'Origine') VALUES {values}")
        conn.commit()
        conn.close()
        logging.info('Writing to SQLite database: "avito_cars.db" is done')
    except Exception as e:
        logging.error(f"Exception occurred while writing to SQLite db: {e}")
