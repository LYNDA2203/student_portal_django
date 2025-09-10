from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm


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
                return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('courses:track_list')
        else:
            error = "Invalid username or password"
    else:
        error = None
    return render(request, 'login.html', {'form': form, 'error': error})

def logout_view(request):
     if request.method in ["POST", "GET"]:
        logout(request)
        return redirect('home')