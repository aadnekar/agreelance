from django.http import HttpResponse
from projects.models import ProjectCategory
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm


def index(request):
    return render(request, "base.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.company = form.cleaned_data.get("company")
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            user.profile.country = form.cleaned_data.get("country")
            user.profile.state = form.cleaned_data.get("state")
            user.profile.city = form.cleaned_data.get("city")
            user.profile.postal_code = form.cleaned_data.get("postal_code")
            user.profile.street_address = form.cleaned_data.get("street_address")
            user.profile.city = form.cleaned_data.get("city")

            user.profile.categories.add(*form.cleaned_data["categories"])
            user.is_active = True
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            from django.contrib import messages

            messages.success(
                request, "Your account has been created, please login to begin."
            )
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "user/signup.html", {"form": form})


def profile_page(request):

    if not request.user.is_authenticated:
        return redirect("signup")

    context = {
        "username": request.user.username.title(),
        "user": request.user,
        "profile": request.user.profile,
        "categories": request.user.profile.categories.all()
    }

    return render(
        request=request,
        template_name="user/profile.html",
        context=context
    )