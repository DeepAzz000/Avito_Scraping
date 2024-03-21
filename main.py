from logging.config import dictConfig
from utils import get_links, get_car_characteristics, navigate_to_website , write_to_csv

def main():

    dictConfig(
        {'version': 1, 'formatters': {'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', }},
        'handlers': {'console': {'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout', 'formatter': 'default'},
        'file': {'class': 'logging.FileHandler', 'filename': 'app.log', 'level': 'INFO', 'formatter': 'default'}},
        'root': {'level': 'INFO', 'handlers': ['console', 'file']}})
    
    try:
        driver = navigate_to_website()
        links = get_links(driver)
        car_data = get_car_characteristics(driver, links)
        write_to_csv(car_data)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
