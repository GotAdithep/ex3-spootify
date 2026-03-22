from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User

def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # Success notification
            messages.success(request, "User created successfully!")
            return redirect("create_user") # Ensure this matches the name in urls.py
        else:
            # Error notification if validation fails (e.g., duplicate username)
            messages.error(request, "Failed to create user. Please check your inputs.")
    else:
        # GET request
        form = UserForm()
    
    # Passing the form to the context allows Django to render field-specific errors if needed later
    return render(request, "user/create-user.html", {"form": form})

def read_user(request):
    # Fetch all user objects from the database
    users = User.objects.all()
    
    # Pass the users to the template
    return render(request, "user/read-user.html", {"users": users})