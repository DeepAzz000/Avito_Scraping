import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime

def navigate_to_website():
    logging.basicConfig(filename='log_history.log', level=logging.INFO)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    website = 'https://www.avito.ma/fr/maroc/voitures-à_vendre'
    driver.get(website)
    logging.info("Navigated to the main page")
    return driver

def get_links(driver):
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

def get_car_characteristics(driver, links):
    logging.info("Getting car elements")
    car_data = []
    for url in links:
        driver.get(url)        
        car_dict = {}
    
        main_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]')))
    
        try:
            car_dict['Name'] = main_info.find_element(By.XPATH, "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/h1").text
            logging.info("Car name found")
        except:
            car_dict['Name'] = None
            logging.info("Car not name found")
        try:
            car_dict['Prix'] = main_info.find_element(By.XPATH, "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p").text
        except:
            car_dict['Prix'] = None
        try:
            car_dict['Localisation'] = main_info.find_element(By.XPATH, "//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span[1]").text
        except:
            car_dict['Localisation'] = None
        
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
                        break
                    else: 
                        car_dict[datatype] = None
                except Exception:
                    car_dict[datatype] = None
                
        car_data.append(car_dict)
    logging.info("Car elements found")
    return car_data

def average_price_per_model(car_data):
    model_data = {}
    for car in car_data:
        model = car['Modèle']
        price = process_price(car['Prix'])
        if price is None: continue
        if model in model_data:
            model_data[model]['total_price'] += price
            model_data[model]['count'] += 1
        else:
            model_data[model] = {'total_price': price, 'count': 1}
    for car in car_data:
        model = car['Modèle']
        if model in model_data:
            car['Average Price'] = model_data[model]['total_price'] / model_data[model]['count']
        else:
            car['Average Price'] = None

def process_price(price):
    if price == "PRIX NON SPÉCIFIÉ": return None    
    price_as_text =  ''.join(char for char in price if char.isdigit())
    try:
        price_as_float = float(price_as_text)
        return price_as_float
    except Exception as e:
        logging.info(f"Exception occured while transforming price: {str(e)}")
        return None

def write_to_csv(car_data):
    timestamp_now_as_text = datetime.now().isoformat().replace(".","_").replace(":","_").replace("-","_")
    csvfile = open(f'./output_files/avito_data_at_{timestamp_now_as_text}.csv', 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(csvfile, fieldnames=car_data[0].keys())
    writer.writeheader()
    for car in car_data:
        writer.writerow(car)
    csvfile.close()
