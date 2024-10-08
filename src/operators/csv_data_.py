import io
import csv
from src import logger

def write_exchange_rates_to_csv_data(exchange_rates):
    logger.info(f">>>>>> Converting to CSV data <<<<<<")

    # Create an in-memory string buffer
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)

    # Write the header with the new Bank and ST Bank column
    writer.writerow(['Timestamp', 'Currency', 'Code', 'Buying Rate', 'Selling Rate', 'Bank', 'ST Bank Code'])

    # Append new data with 'Bank' value
    for row in exchange_rates:
        writer.writerow(row + ['HNB', '7083'])

    # Get the CSV data as a string
    csv_data = csv_buffer.getvalue()
    csv_buffer.close()

    logger.info("Exchange rates successfully converted to CSV data")
    
    return csv_data
