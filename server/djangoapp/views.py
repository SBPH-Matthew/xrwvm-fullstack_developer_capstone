import json
import logging
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Authenticate and log in a user."""
    data = json.loads(request.body)
    username = data.get("userName")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "status": "Failed"})


def logout_request(request):
    """Log out a user."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Register a new user."""
    data = json.loads(request.body)
    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    """Get dealerships (all or by state)."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Get reviews for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint) or []
    for review_detail in reviews:
        sentiment = analyze_review_sentiments(review_detail.get("review", ""))
        review_detail["sentiment"] = sentiment.get("sentiment")
    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    """Get details for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


@csrf_exempt
def add_review(request):
    """Add a review if user is authenticated."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    try:
        pos
