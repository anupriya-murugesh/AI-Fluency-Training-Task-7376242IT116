import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()
BASE_URL = "https://api.groq.com/openai/v1"
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Private Event Venue data
VENUE_PRICES = {"GRAND_HALL": 50000, "GARDEN_TENT": 30000, "ROOFTOP": 40000}

QUESTIONS = [
    "What is the booking price for the ROOFTOP?",
    "What is the total cost for the GRAND_HALL and GARDEN_TENT after a 20% discount?",
    "Is the GRAND_HALL more expensive than the ROOFTOP, and by how much?",
    "Write a short welcome message for our event management company."
]

def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n") 