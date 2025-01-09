import os
from src import logger
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from src.configuration import configuration as config
from datetime import datetime

load_dotenv()

connect_str = os.getenv('connect_str')
container_name_blob = os.getenv('container_name_blob')

def upload_to_blob(csv_data, base_file_name):
    logger.info(">>>>>> Start Uploading to blob <<<<<<")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    def get_next_file_name(base_name, index):
        return f"{base_name}_{index}.csv"
    
    def split_data_into_chunks(data, chunk_size=1400):
        lines = data.strip().split('\n')
        header = lines[0]
        chunks = [lines[i:i + chunk_size] for i in range(1, len(lines), chunk_size)]
        return header, [header + '\n' + '\n'.join(chunk) for chunk in chunks]
    
    # Split the incoming CSV data into chunks
    header, chunks = split_data_into_chunks(csv_data)
    index = 1
    
    for chunk in chunks:
        while True:
            file_name = get_next_file_name(base_file_name, index)
            blob_client = blob_service_client.get_blob_client(container=container_name_blob, blob=file_name)
            
            try:
                existing_data = blob_client.download_blob().readall().decode('utf-8')
                existing_lines = existing_data.strip().split('\n')
                line_count = len(existing_lines) - 1  # Subtract one for the header line
                
                if line_count < 1400:
                    # Combine existing data with the new chunk data
                    new_lines = chunk.strip().split('\n')[1:]  # Skip the header of the new chunk
                    combined_lines = existing_lines + new_lines
                    combined_data = '\n'.join(combined_lines)
                    
                    # Check if combined data exceeds 1400 rows
                    if len(combined_lines) <= 1400:
                        blob_client.upload_blob(combined_data.encode('utf-8'), overwrite=True)
                        break
                    else:
                        # Split the combined data to fit into the current file and prepare the overflow for the next file
                        remaining_lines = combined_lines[1400:]
                        chunk = header + '\n' + '\n'.join(remaining_lines)
                        combined_lines = combined_lines[:1400]
                        combined_data = '\n'.join(combined_lines)
                        blob_client.upload_blob(combined_data.encode('utf-8'), overwrite=True)
                        index += 1
                        continue
            except Exception as e:
                if "BlobNotFound" in str(e):
                    blob_client.upload_blob(chunk.encode('utf-8'))
                    break
                else:
                    logger.error(f"Error while uploading: {e}")
                    raise
            index += 1

    logger.info(">>>>>> Completed Uploading to blob <<<<<<")


## This is about this function 

# For each chunk of data:
# Generate the next file name.
# Get a BlobClient for the current file.
# Try to download existing data from the blob.
# If the blob exists, combine the new chunk with the existing data and check if the combined data exceeds 1400 rows.
# If it exceeds 1400 rows, split the data again and upload only up to 1400 rows.
# If the blob does not exist (catching BlobNotFound exception), upload the chunk as a new blob.
# Log any other exceptions and raise them.
# Increment the index for the next file.
    
def backup_for_reference(html_string: str):
    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(config.container_name_for_reference_backups)
    if not container_client.exists():
        container_client = blob_service_client.create_container(name=config.container_name_for_reference_backups)
    # list existing backups of just our relevant bank
    blob_list = list(container_client.list_blobs())
    for blob in blob_list.copy():
        if config.backup_base_filename not in blob.name:
            blob_list.remove(blob)
    
    # if too many backups, delete the older backups
    sorted_blob_list = sorted(blob_list, key=lambda blob: blob.creation_time, reverse=True)
    if len(sorted_blob_list) > config.backup_pairs_to_keep:
        blobs_to_remove = sorted_blob_list[config.backup_pairs_to_keep:]
        for blob in blobs_to_remove:
            blob_client = container_client.get_blob_client(blob)
            blob_client.delete_blob()
    # upload the new backups
    filename = config.backup_base_filename + str(datetime.now())
    container_client.upload_blob(f'{filename}.html', html_string)