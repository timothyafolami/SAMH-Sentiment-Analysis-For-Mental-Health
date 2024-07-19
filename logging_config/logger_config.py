import logging
import os

# Ensure the log directory exists
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

# Define the logging configuration
logging.basicConfig(
    filename=os.path.join(log_directory, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get a custom logger
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.hasHandlers():
        # Create a file handler
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setLevel(logging.DEBUG)
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
