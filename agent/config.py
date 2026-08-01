import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.1-8b-instant"
# LLM_MODEL = "llama-3.3-70b-versatile"
VERBOSE = True