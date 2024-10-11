# main.py
import asyncio
import platform
from src import logger
from src.utils.log_utils import send_log
from src.connector.blob import upload_to_blob
from src.connector.url import fetch_url_content
from src.operators.extractor_html_list import write_exchange_rates_to_list
from src.operators.extractor_html_dict import write_exchange_rates_to_dict
# from src.operators.save_data import write_exchange_rates_to_csv
from src.operators.csv_data_ import write_exchange_rates_to_csv_data
from src.connector.cosmos_db import write_exchange_rates_to_cosmosdb
from src.operators.insert_json_cosmos import convert_to_cosmos_db_format
from src.configuration.configuration import EXCHANGE_RATES_URL, CSV_FILENAME

async def main():

    try:

        logger.info(">>>Starting the HNB Data Extraction Process<<<")

        # Extract html content from Url
        html_content = fetch_url_content(EXCHANGE_RATES_URL)
        
        # Extract exchange rates from the HTML content to a list
        exchange_rates = write_exchange_rates_to_list(html_content)
        
        # Converting to CSV data to save in blob but not saving it locally
        csv_data = write_exchange_rates_to_csv_data(exchange_rates)
        
        upload_to_blob(csv_data, CSV_FILENAME)
    
        # Convert exchange rates from HTML content to dict
        exchange_rates_dict = write_exchange_rates_to_dict(html_content)

        # Convert to json format
        cosmos_db_documents_json = convert_to_cosmos_db_format(exchange_rates_dict)
        
        # Upload to Cosmos DB
        await write_exchange_rates_to_cosmosdb(cosmos_db_documents_json )

        logger.info(">>>Completion of data ingestion to CosmosDB<<<")
    
        send_log(

            service_type="Azure Function",
            application_name="HNB Exchangerates Collector",
            project_name="Dockit Exchange Rates History",
            project_sub_name="Exchangerates History",
            azure_hosting_name="AI Services",
            developmental_language="Python",
            description="Bank Exchange Rates - Function Application",
            created_by="BrownsAIseviceTest",
            log_print="Successfully completed data ingestion to Cosmos DB.",
            running_within_minutes=1440,
            error_id=0

        )
        logger.info("sent success log to function monitoring service.")

    except Exception as e:
        # send_error_log to monitoring service
        logger.error(f"An error occurred: {e}")

        send_log(

            service_type="Azure Function",
            application_name="HNB Exchangerates Collector",
            project_name="Dockit Exchange Rates History",
            project_sub_name="Exchangerates History",
            azure_hosting_name="AI Services",
            developmental_language="Python",
            description="Bank Exchange Rates - Function Application",
            created_by="BrownsAIseviceTest",
            log_print="An error occurred: " + str(e),
            running_within_minutes=1440,
            error_id=1
        )
        raise

def run_main():
    
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

if __name__ == '__main__':
    run_main()