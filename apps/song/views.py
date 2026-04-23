from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import SongForm, UpdateSongForm
from .models import Song
from apps.song_gen_request.models import SongGenRequest
from apps.song_gen_request.factory import get_generator_strategy
from apps.song_gen_request.utils import create_song_from_clips


@method_decorator(login_required, name='dispatch')
class LibraryView(ListView):
    def get(self, request):
        pending = SongGenRequest.objects.filter(user=request.user, song=None)
        strategy = get_generator_strategy()
        for song_request in pending:
            if not song_request.task_id:
                continue
            try:
                result = strategy.get_status(song_request.task_id)
                if result["status"] == "SUCCESS" and result.get("clips"):
                    create_song_from_clips(song_request, result["clips"])
            except Exception:
                continue

        songs = Song.objects.filter(user=request.user).order_by('-created_at')
        still_pending = SongGenRequest.objects.filter(user=request.user, song=None)
        return render(request, "library.html", {"songs": songs, "pending_requests": still_pending})

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
        song = get_object_or_404(Song, pk=song_id, user=request.user)
        song.delete()
        messages.success(request, "Song deleted successfully!")
        return redirect("library")
