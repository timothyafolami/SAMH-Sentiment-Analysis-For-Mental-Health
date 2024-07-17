import os
import sys
import requests

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging_config.logger_config import get_logger

# Get the logger
logger = get_logger(__name__)

def download_data(url, save_path):
    # Ensure the save directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Send a GET request to the URL
    logger.info(f"Sending GET request to {url}")
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to the specified file
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logger.info(f"Data downloaded successfully and saved to {save_path}")
    else:
        logger.error(f"Failed to download data. Status code: {response.status_code}")

if __name__ == "__main__":
    # URL of the dataset
    dataset_url = "https://raw.githubusercontent.com/timothyafolami/SAMH-Sentiment-Analysis-For-Mental-Health/master/data/Combined_Data.csv"
    
    # Path to save the dataset
    save_file_path = os.path.join("./data", "Combined_Data.csv")

    # Download the dataset
    download_data(dataset_url, save_file_path)
