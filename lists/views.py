from django.shortcuts import redirect, render
from django.urls.base import reverse


def home_page(request):
    if request.method == "POST":
        return render(
            request,
            "home.html",
            {"new_item_text": request.POST["item_text"]},
        )
    return render(request, "home.html")
