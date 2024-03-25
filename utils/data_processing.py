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

def process_km(kilometrage):
    if isinstance(kilometrage, str) and '-' in kilometrage:
        try:
            kilometrage = ''.join(char for char in kilometrage if char.isdigit() or char == '-')
            if '-' in kilometrage:
                avg_kilometrage = sum(map(int, kilometrage.split('-'))) / 2
                return int(avg_kilometrage)
            else:
                return int(kilometrage)
        except Exception as e:
            logging.info(f"Exception occurred while transforming kilometrage: {str(e)}")
            return None
    elif isinstance(kilometrage, str):
        try:
            kilometrage = ''.join(char for char in kilometrage if char.isdigit())
            return int(kilometrage)
        except Exception as e:
            logging.info(f"Exception occurred while transforming kilometrage: {str(e)}")
            return None
    else:
        return None


def get_condition_rating(condition):
    if condition == 'neuf':
        return 10
    elif condition == 'Excellent':
        return 8
    elif condition == 'Très bon':
        return 7
    else:
        return 5

def get_mileage_rating(mileage):
    if mileage < 50000:
        return 9
    elif mileage < 100000:
        return 8
    elif mileage < 150000:
        return 7
    else:
        return 5

def get_origin_rating(origin):
    if origin == 'WW au Maroc':
        return 10
    elif origin == 'Importée neuve':
        return 9
    elif origin == 'Dédouanée':
        return 8
    else:
        return 5

def get_year_model_rating(year_model):
    year_score = 10 - (2024 - year_model)
    return year_score

def get_premiere_main_rating(premiere_main):
    if premiere_main == 'oui':
        return 10
    elif premiere_main == 'non':
        return 5
    else:
        return 5
