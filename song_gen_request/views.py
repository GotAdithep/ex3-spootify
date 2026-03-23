from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SongGenRequestForm, UpdateSongGenRequestForm
from .models import SongGenRequest
# Make sure to import your Song model!
# from song.models import Song 

def create_song_gen_request(request):
    if request.method == "POST":
        form = SongGenRequestForm(request.POST)
        if form.is_valid():
            song_request = form.save(commit=False) 

            song_request.save()
            
            messages.success(request, "Song generation request created successfully!")
            return redirect("create_song_gen_request") 
        else:
            messages.error(request, "Failed to create request. Please check your inputs.")
    else:
        # GET request
        form = SongGenRequestForm()
    
    return render(request, "song_gen_request/create-song-gen-request.html", {"form": form})

def read_song_gen_request(request):
    requests = SongGenRequest.objects.all().order_by('-created_at')
    return render(request, "song_gen_request/read-song-gen-request.html", {"requests": requests})

def update_song_gen_request(request, request_id):
    song_gen_request = get_object_or_404(SongGenRequest, pk=request_id)

    if request.method == "POST":
        form = UpdateSongGenRequestForm(request.POST, instance=song_gen_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Song generation request updated successfully!")
            return redirect("read_song_gen_request")
        else:
            messages.error(request, "Failed to update request. Please check your inputs.")
    else:
        form = UpdateSongGenRequestForm(instance=song_gen_request)

    return render(request, "song_gen_request/update-song-gen-request.html", {"form": form, "req": song_gen_request})

def delete_song_gen_request(request, request_id):
    song_gen_request = get_object_or_404(SongGenRequest, pk=request_id)

    if request.method == "POST":
        song_gen_request.delete()
        messages.success(request, "Song generation request deleted successfully!")
        return redirect("read_song_gen_request")
    
    return render(request, "song_gen_request/delete-song-gen-request.html", {"req": song_gen_request})