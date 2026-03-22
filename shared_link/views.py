from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SharedLinkForm
from .models import SharedLink

def create_shared_link(request):
    if request.method == "POST":
        form = SharedLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shared link created successfully!")
            # Ensure "create_shared_link" matches the name="" in your urls.py
            return redirect("create_shared_link") 
        else:
            messages.error(request, "Failed to create shared link. Please check your inputs.")
    else:
        # GET request
        form = SharedLinkForm()
    
    return render(request, "shared_link/create-shared-link.html", {"form": form})

def read_shared_link(request):
    links = SharedLink.objects.all().order_by('-created_at')
    return render(request, "shared_link/read-shared-link.html", {"links": links})