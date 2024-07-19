from dotenv import load_dotenv
import os, sys
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts.prompt import PromptTemplate

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logging_config.logger_config import get_logger

# Get the logger
logger = get_logger(__name__)

# environment variables
load_dotenv()
groq_api_key=os.getenv('GROQ_API_KEY')

# initialize the ChatGroq object
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

# Sentiment Classification
def sentiment_analyzer(input_text: str) -> str:
    template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a highly specialized AI trained in clinical psychology and mental health assessment. Your task is to analyze textual input and categorize it into one of the following mental health conditions:
    - Normal
    - Depression
    - Suicidal
    - Anxiety
    - Stress
    - Bi-Polar
    - Personality Disorder

    Your analysis should be based on clinical symptoms and diagnostic criteria commonly used in mental health practice. Here are some detailed examples:

    Example 1:
    Text: "I feel an overwhelming sense of sadness and hopelessness. I have lost interest in activities I once enjoyed and find it hard to get out of bed."
    Category: Depression

    Example 2:
    Text: "I constantly worry about various aspects of my life. My heart races, and I experience physical symptoms like sweating and trembling even when there is no apparent danger."
    Category: Anxiety

    Example 3:
    Text: "I have thoughts about ending my life. I feel that there is no other way to escape my pain, and I often think about how I might end it."
    Category: Suicidal

    Example 4:
    Text: "I feel extremely stressed and overwhelmed by my responsibilities. I find it difficult to relax, and I often experience headaches and tension."
    Category: Stress

    Example 5:
    Text: "I go through periods of extreme happiness and high energy, followed by episodes of deep depression and low energy. These mood swings affect my daily functioning."
    Category: Bi-Polar

    Example 6:
    Text: "I have trouble maintaining stable relationships and often experience intense emotional reactions. My self-image frequently changes, and I engage in impulsive behaviors."
    Category: Personality Disorder

    Example 7:
    Text: "I feel generally content and am able to manage my daily activities without significant distress or impairment."
    Category: Normal

    
    Return as out the Category and a brief explanation of your decision in a json format.
    
    Now, analyze the following text and determine the most appropriate category from the list above:
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Human: {input_text}
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    AI Assistant:"""

    sentiment_prompt = PromptTemplate(input_variables=["input_text"], template=template)
    initiator_router = sentiment_prompt | llm | JsonOutputParser()
    output = initiator_router.invoke({"input_text":input_text})
    return output


# making predictions
def predict(text: str) -> str:
    try:
        logger.info("Making prediction...")
        prediction = sentiment_analyzer(text)
        logger.info(f"Prediction: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"An error occurred while making the prediction: {e}")
        return str('The prediction could not be made due to an error., Please try again later.')
    
if __name__ == "__main__":
    # Example text input
    example_text = "I feel incredibly anxious about everything and can't stop worrying"
    
    # Make a prediction
    prediction = predict(example_text)
    print(prediction)