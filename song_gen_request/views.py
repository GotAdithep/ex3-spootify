from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SongGenRequestForm
from .models import SongGenRequest
# Make sure to import your Song model!
# from song.models import Song 

def create_song_gen_request(request):
    if request.method == "POST":
        form = SongGenRequestForm(request.POST)
        if form.is_valid():
            # 1. Pause saving to the database
            song_request = form.save(commit=False) 
            
            # 2. Get or create the actual Song object
            # Note: You need to replace this with your actual logic for getting/creating a song!
            # Example: my_song = Song.objects.create(...) or my_song = Song.objects.get(id=...)
            # song_request.song = my_song  
            
            # 3. Now save the complete object to the database
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