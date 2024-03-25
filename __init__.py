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
    
    if len(sys.argv) < 2:
        print("Usage: python script.py [main_name]")
        sys.exit(1)
    
    chosen_main = sys.argv[1]
    
    if chosen_main == 'scraping':
        scraping_main()
    elif chosen_main == 'stats':
        stats_main()
    else:
        print("Invalid main name. Please choose 'scraping' or 'stats'.")
        sys.exit(1)
