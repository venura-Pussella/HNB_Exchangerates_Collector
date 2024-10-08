import os
import csv
from src import logger
from src.operators.helper import ensure_directory_exists
from src.configuration.configuration import CSV_DIR , CSV_FILENAME

def write_exchange_rates_to_csv(exchange_rates, csv_filename):
        
        logger.info(f">>>>>> Saving the extracted data to CSV file: {CSV_FILENAME} <<<<<<")

        # Check if the directory exists, create it if not
        ensure_directory_exists(CSV_DIR)

        # Construct the full path to the CSV file
        csv_path = os.path.join(CSV_DIR, csv_filename)

        # Use 'a+' mode for append and read
        with open(csv_path, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Check if the file is empty (if it's a new file, write the header)
            csvfile.seek(0)  # Move cursor to the start of the file
            first_line = csvfile.readline()
            if not first_line:
                writer.writerow(['Timestamp', 'Currency', 'Code', 'Buying Rate', 'Selling Rate'])

            # Append new data
            writer.writerows(exchange_rates) 

        logger.info(f"Exchange rates successfully appended to {csv_filename}")
