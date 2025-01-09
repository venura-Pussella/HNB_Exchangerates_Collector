import os

# CSV data saving path
CSV_DIR = os.path.join('data', 'csv')

# CSV data saving name
CSV_FILENAME = 'HNB_exchange_rates'

# SQL Table name
SQL_TABLE_NAME = 'exchange_rates'

# HNB bank exchange rate url 
EXCHANGE_RATES_URL = 'https://www.hnb.net/exchange-rates'

container_name_for_reference_backups = 'bank-exchange-rates-reference-backups'
backup_base_filename = 'HNB'
backup_pairs_to_keep = 28