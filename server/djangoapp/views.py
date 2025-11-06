from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle user login"""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    user = authenticate(username=username, password=password)

    data = {"userName": username}
    if user is not None:
        login(request, user)
        data["status"] = "Authenticated"

    return JsonResponse(data)


def logout_request(request):
    """Handle logout"""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Handle user registration"""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    try:
        User.objects.get(username=username)
        return JsonResponse({
            "status": 200,
            "dealers": dealerships,
        })
    except User.DoesNotExist:
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
    """Fetch all dealerships or by state"""
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Fetch reviews and analyze sentiment"""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review in reviews:
            response = analyze_review_sentiments(review["review"])
            review["sentiment"] = response.get("sentiment", "neutral")
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """Fetch a dealer by ID"""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealer = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    """Add a new dealer review"""
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )
    return JsonResponse({"status": 403, "message": "Unauthorized"})
