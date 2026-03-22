from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserForm, UpdateUserForm
from .models import User

def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect("create_user")
        else:
            messages.error(request, "Failed to create user. Please check your inputs.")
    else:
        form = UserForm()

    return render(request, "user/create-user.html", {"form": form})

def read_user(request):
    users = User.objects.all()
    return render(request, "user/read-user.html", {"users": users})

def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect("read_user")
        else:
            messages.error(request, "Failed to update user. Please check your inputs.")
    else:
        form = UpdateUserForm(instance=user)

    return render(request, "user/update-user.html", {"form": form, "user": user})