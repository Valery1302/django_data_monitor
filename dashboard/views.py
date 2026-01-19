from django.shortcuts import render
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def index(request):
    # (si quieres mantener permission_required, lo vemos luego)
    try:
        r = requests.get(settings.API_URL, timeout=10)
        r.raise_for_status()

        data = r.json()

        # soporta lista o dict tipo {"results":[...]}
        posts = data.get("results", []) if isinstance(data, dict) else data
        if not isinstance(posts, list):
            posts = []

        api_error = None

    except Exception as e:
        posts = []
        api_error = f"No se pudo cargar la API: {e.__class__.__name__}"

    context = {
        "title": "Landing Page Dashboard",
        "total_responses": len(posts),
        "posts": posts,
        "api_error": api_error,
    }
    return render(request, "dashboard/index.html", context)
