import sys
from main.scraping_main import main as scraping_main
from main.stats_main import main as stats_main
from logging.config import dictConfig

if __name__ == "__main__":
    
    dictConfig(
    {'version': 1, 'formatters': {'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', }},
    'handlers': {'console': {'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout', 'formatter': 'default'},
    'file': {'class': 'logging.FileHandler', 'filename': 'app.log', 'level': 'INFO', 'formatter': 'default'}},
    'root': {'level': 'INFO', 'handlers': ['console', 'file']}})
    
    if len(sys.argv) < 3:
        print("Usage: python script.py [main_name], [saving_format]")
        sys.exit(1)
    
    chosen_main = sys.argv[1]
    to_db = "save to db"
    to_csv = "save to csv"
    if chosen_main == 'scrape':
        chosen_main = sys.argv[2]
        if chosen_main == 'to_db':
            save_as = to_db
            scraping_main(save_as)
        elif chosen_main == 'to_csv':
            save_as = to_csv
            scraping_main(save_as)
    elif chosen_main == 'stats':
        stats_main()
    else:
        print("Invalid main name. Please choose 'scrape' or 'stats'. If scrape then choose 'to_db' or 'to_csv' to save the data")
        sys.exit(1)
