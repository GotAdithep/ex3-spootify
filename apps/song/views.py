from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import SongForm, UpdateSongForm
from .models import Song

class CreateSongView(CreateView):
    def get(self, request):
        return render(request, "song/create-song.html")
    
    def post(self, request):
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Song created successfully!")
            return redirect("create_song") 
        else:
            messages.error(request, "Failed to create song. Please check your inputs.")

class ListSongView(ListView):
    def get(self, request):
        songs = Song.objects.all().order_by('-created_at') # Order by newest first
        return render(request, "song/read-song.html", {"songs": songs}) 

class UpdateSongView(UpdateView):
    def get(self, request, song_id):
        return render(request, "song/update-song.html")
    
    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        form = UpdateSongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, "Song updated successfully!")
            return redirect("read_song")
        else:
            messages.error(request, "Failed to update song. Please check your inputs.")
        

class DeleteSongView(DeleteView):
    def get(self, request, song_id):
        return render(request, "song/delete-song.html")
    
    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        song.delete()
        messages.success(request, "Song deleted successfully!")
        return redirect("read_song")
