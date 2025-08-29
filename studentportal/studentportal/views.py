from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate


def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the new user
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:  # Only registered users with correct credentials
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password"
    else:
        error = None

    return render(request, 'login.html', {'error': error})