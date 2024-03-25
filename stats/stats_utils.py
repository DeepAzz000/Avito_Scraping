import pandas as pd
import logging

def process_price(price):
    if price == "PRIX NON SPÉCIFIÉ":
        return None
    price_as_text = ''.join(char for char in price if char.isdigit())
    try:
        price_as_float = float(price_as_text)
        return price_as_float
    except Exception as e:
        logging.info(f"Exception occurred while transforming price: {str(e)}")
        return None

def calculate_average_price(Row_Data_csv_file_path):
    try:
        df = pd.read_csv(Row_Data_csv_file_path)
        df['Prix'] = df['Prix'].apply(process_price)
        price_stats = df.groupby('Modèle')['Prix'].agg(['mean', 'min', 'max']).round(2)
        price_stats.reset_index(inplace=True)
        price_stats = price_stats.to_dict(orient='records')
        return price_stats        
    except Exception as e:
        print(f"Error occurred while calculating the average price: {e}")
        return None

def car_count_per_model_location(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
        car_count = df.groupby(['Modèle', 'Location']).size().reset_index(name='Count')
        car_count = car_count.to_dict(orient='records')
        return car_count 
    except Exception as e:
        print(f"Error occurred while calculating the average price: {e}")
        return None
