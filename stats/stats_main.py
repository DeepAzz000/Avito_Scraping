from scraping.scraping_utils import write_to_csv
from stats.stats_utils import calculate_average_price, car_count_per_model_location

def main():
    Row_Data_csv_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\Avito_Data.csv'
    price_stats = calculate_average_price(Row_Data_csv_file_path)

    price_stats_csv_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\Price_stats.csv'
    write_to_csv(price_stats, price_stats_csv_file_path)

    car_count = car_count_per_model_location(Row_Data_csv_file_path)

    car_count_csv_file_path = 'C:\\Users\\Public\\Avito_Scraping\\output_files\\Car_count_per_model_location.csv'
    write_to_csv(car_count, car_count_csv_file_path)

if __name__ == '__name__':
    main()