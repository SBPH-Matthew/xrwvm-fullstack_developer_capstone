import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("backend_url", default="http://localhost:3030")
SENTIMENT_ANALYZER_URL = os.getenv(
    "sentiment_analyzer_url",
    default="http://localhost:5050/",
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = BACKEND_URL + endpoint + "?" + params
    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Network exception occurred: {err}")


def analyze_review_sentiments(text):
    request_url = SENTIMENT_ANALYZER_URL + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = BACKEND_URL + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Network exception occurred: {err}")
