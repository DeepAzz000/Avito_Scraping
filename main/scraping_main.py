import logging
from utils.scraping_utils import get_links, get_car_characteristics, navigate_to_website, write_to_csv, write_to_db
import threading

def process_page(page_number, save_as):
    try:
        driver = navigate_to_website(page_number)
        links = get_links(driver)
        car_data = get_car_characteristics(driver, links)
        output_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\avito_raw_data.csv'
        if save_as == "save to db":
            write_to_db(car_data)
        elif save_as == "save to csv":
            write_to_csv(car_data, output_file_path)
        driver.quit()
    except Exception as e:
        logging.error(f"Error processing page {page_number}: {e}")

def main(save_as):
    
    current_page = 1
    max_pages = 1
    threads = []

    while current_page <= max_pages:
        thread = threading.Thread(target=process_page, args=(current_page,save_as))
        thread.start()
        threads.append(thread)
        current_page += 1

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
