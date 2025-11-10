from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from mentor.models import UserProfile, Student
from django.contrib.auth.models import User
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # --- Create base user ---
            user = form.save(commit=False)
            user.username = user.username.strip().lower()
            user.set_password(form.cleaned_data["password1"])

            role = form.cleaned_data.get("role")

            # --- Assign staff/superuser flags based on role ---
            if role == "student":
                user.is_staff = False
                user.is_superuser = False
            elif role == "mentor":
                user.is_staff = True
                user.is_superuser = True

            user.save()

            # --- Create or update UserProfile ---
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            # --- Handle student registration ---
            if role.lower() == "student":
                # Get mentor username from form if provided (optional field)
                mentor_username = form.cleaned_data.get("mentor_username")

                # Try to find mentor user (case-insensitive)
                mentor_user = None
                if mentor_username:
                    mentor_user = User.objects.filter(username__iexact=mentor_username).first()
                    if not mentor_user:
                        messages.warning(request, f"⚠️ Mentor '{mentor_username}' not found. Student will be unassigned.")

                # --- Get or create Student record ---
                student, created = Student.objects.get_or_create(
                    user=user,
                    defaults={
                        "full_name": user.get_full_name() or user.username,
                        "mentor": mentor_user
                    }
                )

                # Update mentor if already existed
                if not created and mentor_user:
                    student.mentor = mentor_user
                    student.save()

                print(f"✅ Student record linked: {student.full_name} → Mentor: {student.mentor or 'None'}")

            print(f"✅ User created: {user.username}, role: {profile.role}")
            messages.success(request, "✅ Registration successful! You can now log in.")
            return redirect("login")

        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    error = None    
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        username = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password")
        print("Authencation :",username)
        
        user = authenticate(request, username=username, password=password)
        print("Authencation :",user)
        
        if user:
            print("🔹 Authenticated user:", user.username)
            if hasattr(user, "userprofile"):
                print("🔹 Role:", user.userprofile.role)
            else:
                print("❌ No UserProfile linked to this user")
            # Log the user in
            login(request, user)
            print("logged in successfully")

            # Ensure user profile exists
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            print("user_profile created successfully",user_profile.role)
            
            if user_profile.role == "student":
                
                student, _ = Student.objects.get_or_create(
                    user=user,
                    defaults={"full_name": user.get_full_name() or user.username}
                )
                print("student profile created or exsists",student)
                return redirect("student:student_dashboard")

            elif user_profile.role == "mentor":
                return redirect("courses:track_list")

            else:
                error = "Unknown user role."

        else:
            error = "Invalid username or password."

    return render(request, "login.html", {"form": form, "error": error})

def logout_view(request):
     if request.method in ["POST", "GET"]:
        logout(request)
        return redirect('home')