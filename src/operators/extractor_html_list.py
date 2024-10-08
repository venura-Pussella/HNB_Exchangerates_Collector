from bs4 import BeautifulSoup
import datetime
from src import logger

def write_exchange_rates_to_list(html_content):
        
        logger.info(">>>>>> Extracting exchange rates from the HTML content <<<<<<")

        soup = BeautifulSoup(html_content, 'html.parser')
        
        table = soup.find('table')
        if not table:
            raise ValueError("No table found in HTML content")

        rows = table.find_all('tr')
        if len(rows) < 2:
            raise ValueError("Table has no data rows")

        exchange_rates = []
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Assuming the first row is the header, the rest are data rows
        for i, row in enumerate(rows[1:]):  # Skip the header row
            cols = row.find_all('td')
            if len(cols) != 4:
                logger.warning(f"Skipping row {i+1} due to unexpected number of columns: {len(cols)}")
                continue

            currency = cols[0].text.strip()
            code = cols[1].text.strip()
            buying_rate = cols[2].text.strip()
            selling_rate = cols[3].text.strip()

            # Validate that the data is not empty
            if not (currency and code and buying_rate and selling_rate):
                logger.warning(f"Skipping row {i+1} due to empty fields")
                continue

            exchange_rates.append([current_datetime, currency, code, buying_rate, selling_rate])

        if not exchange_rates:
            raise ValueError("No valid data extracted from the table")
        
        logger.info(">>>>>> Extracted exchange rates successfully <<<<<<")
        
        return exchange_rates

    