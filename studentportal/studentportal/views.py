from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from mentor.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create the user instance
            user = form.save(commit=False)
            user.username = user.username.strip().lower()

            # Hash password securely
            user.set_password(form.cleaned_data["password1"])

            # Handle role-specific flags
            role = form.cleaned_data.get("role")
            if role == "student":
                user.is_staff = False
                user.is_superuser = False
            elif role == "mentor":
                user.is_staff = True  # optional: allow mentors staff privileges
                user.is_superuser = True

            user.save()

            # Create the linked profile
            UserProfile.objects.create(user=user, role=role)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    error = None
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        username = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if hasattr(user, "userprofile"):
                if user.userprofile.role == "student":
                    return redirect("student:student_dashboard")
                elif user.userprofile.role == "mentor":
                    return redirect("courses:track_list")
                else:
                    error = "Unknown user role."
            else:
                error = "User profile not found."

        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"form": form, "error": error})

def logout_view(request):
     if request.method in ["POST", "GET"]:
        logout(request)
        return redirect('home')