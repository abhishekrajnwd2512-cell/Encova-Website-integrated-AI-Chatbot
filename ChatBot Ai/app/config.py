from dotenv import load_dotenv 
import os

load_dotenv() 

class Config:
    APP_NAME = os.getenv("APP_NAME")
    MODEL = os.getenv("MODEL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    INPUT_COST_PER_MILLION = 1.50
    OUTPUT_COST_PER_MILLION = 7.50  


