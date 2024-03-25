from utils.scraping_utils import write_to_csv
from utils.stats_utils import price_statistics, car_count_per_brand_location, plot_of_price_vs_mileage, score

def main():
    avito_raw_data = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\avito_raw_data.csv'
    
    price_stats = price_statistics(avito_raw_data)
    price_stats_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\price_statistics.csv'
    write_to_csv(price_stats, price_stats_file_path)
    
    car_count = car_count_per_brand_location(avito_raw_data)
    car_cnt_brand_location = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\car_count_per_brand_location.csv'
    write_to_csv(car_count, car_cnt_brand_location)
    
    plot_of_price_vs_mileage(avito_raw_data)
    
    rating_coefficients = {'condition': 0.5, 'mileage': 0.2, 'origin': 0.1, 'year_model': 0.1, 'premiere_main': 0.1}
    score(avito_raw_data, rating_coefficients)

if __name__ == '__name__':
    main()