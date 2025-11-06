import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("backend_url", "http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    default="http://localhost:5050/",
)


def get_request(endpoint, **kwargs):
    """Perform a GET request to the backend."""
    params = "&".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
    request_url = f"{BACKEND_URL}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url, timeout=10)
        return response.json()
    except requests.RequestException as exc:
        print(f"Network exception occurred: {exc}")
        return None


def analyze_review_sentiments(text):
    """Call sentiment analyzer microservice."""
    request_url = f"{SENTIMENT_ANALYZER_URL}analyze/{text}"
    try:
        response = requests.get(request_url, timeout=10)
        return response.json()
    except requests.RequestException as err:
        print(f"Sentiment API error: {err}")
        return {"sentiment": "neutral"}


def post_review(data_dict):
    """Post a review to backend service."""
    request_url = f"{BACKEND_URL}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=10)
        return response.json()
    except requests.RequestException as exc:
        print(f"Network exception occurred: {exc}")
        return None
