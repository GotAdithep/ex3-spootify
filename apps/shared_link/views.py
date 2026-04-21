from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import SharedLinkForm, UpdateSharedLinkForm
from .models import SharedLink

class CreateSharedLinkView(CreateView):
    def get(self, request):
        form = SharedLinkForm()
        return render(request, "shared_link/create-shared-link.html", {"form": form})
    
    def post(self, request):
        form = SharedLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shared link created successfully!")
        else:
            messages.error(request, "Failed to create shared link. Please check your inputs.")
        return redirect("create_shared_link") 
        

class ListSharedLinkView(CreateView):
    def get(self, request):
        links = SharedLink.objects.all().order_by('-created_at')
        return render(request, "shared_link/read-shared-link.html", {"links": links})

class UpdateSharedLinkView(UpdateView):
    def get(self, request, link_id):
        shared_link = get_object_or_404(SharedLink, pk=link_id)
        form = UpdateSharedLinkForm(instance=shared_link)
        return render(request, "shared_link/update-shared-link.html", {"form": form, "link": shared_link})
    
    def post(self, request, link_id):
        shared_link = get_object_or_404(SharedLink, pk=link_id)
        form = UpdateSharedLinkForm(request.POST, instance=shared_link)
        if form.is_valid():
            form.save()
            messages.success(request, "Shared link updated successfully!")
            return redirect("read_shared_link")
        else:
            messages.error(request, "Failed to update shared link. Please check your inputs.")

class DeleteSharedLinkView(DeleteView):
    def get(self, request, link_id):
        return render(request, "shared_link/delete-shared-link.html")
    
    def post(self, request, link_id):
        shared_link = get_object_or_404(SharedLink, pk=link_id)
        shared_link.delete()
        messages.success(request, "Shared link deleted successfully!")
        return redirect("read_shared_link")
