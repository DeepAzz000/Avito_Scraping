from utils import get_links, get_car_characteristics, average_price_per_model, write_to_csv, navigate_to_website

def main():
    
    try:
        driver = navigate_to_website()
        links = get_links(driver)
        car_data = get_car_characteristics(driver, links)
        average_price_per_model(car_data)
        write_to_csv(car_data)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
