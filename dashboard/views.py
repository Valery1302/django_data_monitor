from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import requests

@login_required
@permission_required("dashboard.index_viewer", raise_exception=True)
def index(request):
    error = None
    posts = []

    try:
        r = requests.get(settings.API_URL, timeout=8)
        r.raise_for_status()  # si es 403/500 etc, lanza error
        posts = r.json()      # si no es JSON, lanza error
    except Exception as e:
        error = str(e)

    data = {
        "title": "Landing Page Dashboard",
        "total_responses": len(posts),
        "error": error,
        "posts": posts,
    }
    return render(request, "dashboard/index.html", data)
