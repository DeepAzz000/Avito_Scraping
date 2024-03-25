import pandas as pd
import matplotlib.pyplot as plt
from utils.data_processing import process_price, process_km, get_condition_rating, get_mileage_rating, get_origin_rating, get_year_model_rating, get_premiere_main_rating


def price_statistics(avito_raw_data):
    try:
        df = pd.read_csv(avito_raw_data)
        df['Prix'] = df['Prix'].apply(process_price)
        price_stats = df.groupby('Modèle')['Prix'].agg(['mean', 'min', 'max']).round(2)
        price_stats.reset_index(inplace=True)
        price_stats = price_stats.to_dict(orient='records')
        return price_stats        
    except Exception as e:
        print(f"Error occurred in the price statistics: {e}")
        return None

def car_count_per_brand_location(avito_raw_data):
    try:
        df = pd.read_csv(avito_raw_data)
        car_count = df.groupby(['Modèle', 'Location']).size().reset_index(name='Count')
        car_count = car_count.to_dict(orient='records')
        return car_count 
    except Exception as e:
        print(f"Error occurred in the car count per model location: {e}")
        return None

def plot_of_price_vs_mileage(avito_raw_data):
    try:
        df = pd.read_csv(avito_raw_data)
        df['Prix'] = df['Prix'].apply(process_price)
        df['Kilométrage'] = df['Kilométrage'].apply(process_km)
        plt.scatter(df['Kilométrage'], df['Prix'])
        plt.xlabel('Mileage')
        plt.ylabel('Price')
        plt.title('Price vs. Mileage')
        plt.savefig('./output_files/average_kilometrage_plot.png', dpi=300)
    except Exception as e:
        print(f"Error occurred int the plot of price vs mileage: {e}")
        return None    

def score(avito_raw_data, rating_coefficients):
    df = pd.read_csv(avito_raw_data)
    df['condition_rating'] = df['État'].apply(get_condition_rating)
    df['Kilométrage'] = df['Kilométrage'].apply(process_km)
    df['mileage_rating'] = df['Kilométrage'].apply(get_mileage_rating)
    df['origin_rating'] = df['Origine'].apply(get_origin_rating)
    df['year_model_rating'] = df['Année-Modèle'].apply(get_year_model_rating)
    df['premiere_main_rating'] = df['Première main'].apply(get_premiere_main_rating)
    
    condition_coeff = rating_coefficients['condition']
    mileage_coeff = rating_coefficients['mileage']
    origin_coeff = rating_coefficients['origin']
    year_coeff = rating_coefficients['year_model']
    premiere_main_coeff = rating_coefficients['premiere_main']

    df['overall_rating'] = df['condition_rating'] * condition_coeff + df['mileage_rating'] * mileage_coeff + df['origin_rating'] * origin_coeff + df['year_model_rating'] * year_coeff + df['premiere_main_rating'] * premiere_main_coeff
        
    df.to_csv(avito_raw_data, index=False)
