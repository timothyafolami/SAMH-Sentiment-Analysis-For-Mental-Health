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
    logger.setLevel(logging.INFO)
    
    # Create a console handler (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Add the console handler to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger
