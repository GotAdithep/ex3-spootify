from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import UserForm, UpdateUserForm
from .models import User

class CreateUserView(CreateView):
    def get(self, request):
        return render(request, "user/create-user.html")
    
    def post(self, request):
        form = UserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
        else:
            messages.error(request, "Failed to create user. Please check your inputs.")
        return redirect("create_user")

class ListUserView(ListView):
    def get(self, request):
        users = User.objects.all()
        return render(request, "user/read-user.html", {"users": users})

class UpdateUserView(UpdateView):
    def get(self, request, user_id):
        return render(request, "user/update-user.html")
    
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect("read_user")
        else:
            messages.error(request, "Failed to update user. Please check your inputs.")
        

class DeleteUserView(DeleteView):
    def get(self, request, user_id):
        return render(request, "user/delete-user.html")
    
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect("read_user")

