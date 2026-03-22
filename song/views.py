from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SongForm
from .models import Song

def create_song(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Song created successfully!")
            # Ensure "create_song" matches the name="" in your urls.py
            return redirect("create_song") 
        else:
            messages.error(request, "Failed to create song. Please check your inputs.")
    else:
        # GET request
        form = SongForm()
    
    # Pass the form to the template so we can render the user dropdown
    return render(request, "song/create-song.html", {"form": form})

def read_song(request):
    songs = Song.objects.all().order_by('-created_at') # Order by newest first
    return render(request, "song/read-song.html", {"songs": songs})