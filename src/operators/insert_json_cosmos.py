import uuid
from src import logger

def convert_to_cosmos_db_format(exchange_rates):
    logger.info(">>>>>> Converting to json format <<<<<<")

    cosmos_db_documents = []
    for rate in exchange_rates:
        # Generate a unique id for each document
        rate_document = {
            "id": str(uuid.uuid4()),
            "timestamp": rate['timestamp'],
            "currency": rate['currency'],
            "code": rate['code'],
            "buying_rate": float(rate['buying_rate']),
            "selling_rate": float(rate['selling_rate']),
            "bank": "HNB",
            "st_bank_code": "7083"
        }
        cosmos_db_documents.append(rate_document)

    logger.info(">>>>>> Converted to json format successfully <<<<<<")
    
    return cosmos_db_documents
