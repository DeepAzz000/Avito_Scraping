from concurrent.futures import ThreadPoolExecutor
from utils.scraping_utils import navigate_to_website, get_links, get_car_characteristics, write_to_csv, write_to_db
import logging
from time import perf_counter
import threading

def process_page(page, save_as):
    try:
        logging.info(f"Processing page {page}")
        start = perf_counter()
        driver = navigate_to_website(page)
        links = get_links(driver)
        car_data = get_car_characteristics(driver, links)
        end = perf_counter()
        logging.info(f"Total time: {end-start}")
        if save_as == "save to db":
            write_to_db(car_data)
        elif save_as == "save to csv":
            output_file_path = 'C:\\Users\\Public\\Avito_Scraping.worktrees\\v2\\output_files\\avito_raw_data.csv'
            write_to_csv(car_data, output_file_path)
    except Exception as e:
        logging.error(f"Error processing page {page}: {e}")

def main(save_as):
    threads = []    
    thread1 = threading.Thread(target=process_page, args=(1, save_as))
    thread2 = threading.Thread(target=process_page, args=(2, save_as))
    # thread3 = threading.Thread(target=process_page, args=(3, save_as))
    # thread4 = threading.Thread(target=process_page, args=(4, save_as))
    thread1.start()
    thread2.start()
    # thread3.start()
    # thread4.start()
    threads.append(thread1)
    threads.append(thread2)
    # threads.append(thread3)
    # threads.append(thread4)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
