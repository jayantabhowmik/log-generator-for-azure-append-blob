from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient, BlobType
import logging
import time
import datetime

# Configuration
connect_str = "<connection-string>"  # Azure Storage account connection string
container_name = "<container_name>"
blob_name = "<blob_name>"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

# Ensure the container exists
try:
    container_client.create_container()
except Exception as e:
    print(f"Container already exists: {e}")

# Get the append blob client
blob_client = container_client.get_blob_client(blob_name)

# Ensure the blob exists
if not blob_client.exists():
    blob_client.create_append_blob()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

# Function to generate detailed log events
def generate_log_event():
    for i in range(100):
        log_message = f"Log event {i}: Sample log entry."
        detailed_log = create_detailed_log(log_message)
        logger.info(detailed_log)
        append_to_blob(detailed_log)
        time.sleep(1)

# Function to create detailed log format
def create_detailed_log(log_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    detailed_log = f"""
{timestamp} Request URL: 'https://storagedemo007.blob.core.windows.net/test/log-capture?comp=REDACTED&sv=REDACTED&ss=REDACTED&srt=REDACTED&sp=REDACTED&se=REDACTED&st=REDACTED&spr=REDACTED&sig=REDACTED'
Request method: 'PUT'
Request headers:
    'Content-Length': '31'
    'x-ms-version': 'REDACTED'
    'Content-Type': 'application/octet-stream'
    'Accept': 'application/xml'
    'User-Agent': 'azsdk-python-storage-blob/12.20.0 Python/3.9.6 (macOS-14.5-x86_64-i386-64bit)'
    'x-ms-date': 'REDACTED'
    'x-ms-client-request-id': '38bfe13c-2cf4-11ef-be9c-acde48001122'
A body is sent with the request
{timestamp} Response status: 201
Response headers:
    'Content-Length': '0'
    'Last-Modified': 'Mon, 17 Jun 2024 21:54:51 GMT'
    'ETag': '"0x8DC8F181D481CAA"'
    'Server': 'Windows-Azure-Blob/1.0 Microsoft-HTTPAPI/2.0'
    'x-ms-request-id': '7a49acba-d01e-0063-2300-c126ef000000'
    'x-ms-client-request-id': '38bfe13c-2cf4-11ef-be9c-acde48001122'
    'x-ms-version': 'REDACTED'
    'x-ms-content-crc64': 'REDACTED'
    'x-ms-blob-append-offset': 'REDACTED'
    'x-ms-blob-committed-block-count': 'REDACTED'
    'x-ms-request-server-encrypted': 'REDACTED'
    'Date': 'Mon, 17 Jun 2024 21:54:50 GMT'
Appended log: {log_message}
"""
    return detailed_log

# Function to append log event to blob
def append_to_blob(log_message):
    try:
        blob_client.append_block(log_message + "\n")
        print(f"Appended log: {log_message}")
    except Exception as e:
        print(f"Error appending to blob: {e}")

if __name__ == "__main__":
    generate_log_event()
