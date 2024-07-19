import os, sys
from supabase import create_client, Client

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logging_config.logger_config import get_logger

# Get the logger
logger = get_logger(__name__)


#connecting to the database
url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_API_KEY")
supabase: Client = create_client(url, key)

# creating a function to update the database
def insert_db(data: dict, table='Interaction History'):
    try:
        logger.info(f"Inserting data into the database: {data}")
        response = supabase.table(table).insert(data).execute()
        logger.info(f"Data inserted successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Error inserting data into the database: {e}")
        return None
    
if __name__ == "__main__":
    # Test the insert_db function
    data = {
    "Input_text" : "I feel incredibly anxious about everything and can't stop worrying",
    "Model_prediction" : "Anxiety",
    "Llama_3_Prediction" : "Anxiety",
    "Llama_3_Explanation" : "After my analysis, i concluded that the user is suffering from anxiety",
    "User Rating" : 5,
    }
    
    response = insert_db(data)
    print(response)
    