from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SongForm, UpdateSongForm
from .models import Song

def create_song(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Song created successfully!")
            return redirect("create_song") 
        else:
            messages.error(request, "Failed to create song. Please check your inputs.")
    else:
        # GET request
        form = SongForm()
    

    return render(request, "song/create-song.html", {"form": form})

def read_song(request):
    songs = Song.objects.all().order_by('-created_at') # Order by newest first
    return render(request, "song/read-song.html", {"songs": songs}) 

def update_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    if request.method == "POST":
        form = UpdateSongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, "Song updated successfully!")
            return redirect("read_song")
        else:
            messages.error(request, "Failed to update song. Please check your inputs.")
    else:
        form = UpdateSongForm(instance=song)

    return render(request, "song/update-song.html", {"form": form, "song": song})

def delete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    if request.method == "POST":
        song.delete()
        messages.success(request, "Song deleted successfully!")
        return redirect("read_song")
    
    return render(request, "song/delete-song.html", {"song": song})