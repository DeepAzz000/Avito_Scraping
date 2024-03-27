import logging
from utils.scraping_utils import get_links, get_car_characteristics, navigate_to_website, write_to_csv
import threading

def process_page(page_number):
    try:
        driver = navigate_to_website(page_number)
        links = get_links(driver)
        car_data = get_car_characteristics(driver, links)
        output_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\avito_raw_data.csv'
        write_to_csv(car_data, output_file_path)
        driver.quit()
    except Exception as e:
        logging.error(f"Error processing page {page_number}: {e}")

def main():
    current_page = 1
    max_pages = 2
    threads = []

    while current_page <= max_pages:
        thread = threading.Thread(target=process_page, args=(current_page,))
        thread.start()
        threads.append(thread)
        current_page += 1

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
