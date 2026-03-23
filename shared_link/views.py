from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SharedLinkForm, UpdateSharedLinkForm
from .models import SharedLink

def create_shared_link(request):
    if request.method == "POST":
        form = SharedLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shared link created successfully!")
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

def update_shared_link(request, link_id):
    shared_link = get_object_or_404(SharedLink, pk=link_id)

    if request.method == "POST":
        form = UpdateSharedLinkForm(request.POST, instance=shared_link)
        if form.is_valid():
            form.save()
            messages.success(request, "Shared link updated successfully!")
            return redirect("read_shared_link")
        else:
            messages.error(request, "Failed to update shared link. Please check your inputs.")
    else:
        form = UpdateSharedLinkForm(instance=shared_link)

    return render(request, "shared_link/update-shared-link.html", {"form": form, "link": shared_link})

def delete_shared_link(request, link_id):
    shared_link = get_object_or_404(SharedLink, pk=link_id)

    if request.method == "POST":
        shared_link.delete()
        messages.success(request, "Shared link deleted successfully!")
        return redirect("read_shared_link")
    
    return render(request, "shared_link/delete-shared-link.html", {"link": shared_link})