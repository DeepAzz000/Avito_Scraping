import logging
from scraping.scraping_utils import get_links, get_car_characteristics, navigate_to_website , write_to_csv

def main():

    current_page = 1
    max_pages = 2
    while current_page <= max_pages:
        driver = navigate_to_website(current_page)
        try:
            links = get_links(driver)
        except Exception:
            logging.info("Couldn't navigate to main element")
        car_data = get_car_characteristics(driver, links)
        csv_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\Avito_Data.csv'
        
        write_to_csv(car_data, csv_file_path)
        current_page += 1
        driver.quit()

if __name__ == "__main__":
    main()
