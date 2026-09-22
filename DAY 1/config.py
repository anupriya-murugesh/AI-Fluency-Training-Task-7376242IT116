"""Shared configuration: chooses the LLM provider and holds the canteen data."""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "ollama":
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")

elif PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

elif PROVIDER == "huggingface":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

else:
    raise SystemExit(
        f"Unknown PROVIDER '{PROVIDER}'. "
        f"Use ollama, groq or huggingface."
    )

if not API_KEY:
    raise SystemExit(
        f"No API key found for PROVIDER={PROVIDER}. "
        f"Check your .env file."
    )

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# Private canteen data

MENU_PRICES = {
    "Veg Sandwich": 60,
    "Masala Dosa": 50,
    "Fried Rice": 100,
    "Lemon Juice": 30,
    "Coffee": 25,
    "Samosa": 20
}

QUESTIONS = [
    "What is the price of Fried Rice?",
    "What is the total cost of Coffee and Lemon Juice?",
    "I have ₹150. Can I buy Fried Rice and Coffee?",
    "Write a two-line welcome message for canteen visitors."
]

def banner(system_name):
    print(
        f"\n=== {system_name} | "
        f"provider: {PROVIDER} | "
        f"model: {MODEL} ===\n"
    )