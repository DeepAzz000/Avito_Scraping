# OVERVIEW

This project aims to scrape car listings from the Avito website. It retrieves car characteristics such as name, price, location, and additional details, and saves them into a CSV file or a SQLite database for further analysis.

# HOW TO USE

To run this program, call the file __avito_scrapper__.py with the arguments :  

   * __scrape__: to scrape data 
      * __to_db__: to generate SQLite database file
         Setup the database:
            Run the SQLite3 command-line tool and specify the database file: sqlite3 avito_cars.db 
            on the SQLite3 prompt, execute the SQL script: .read database_set_up.sql

      * __to_csv__: to generate csv file
   * __stats__: to generate statistics