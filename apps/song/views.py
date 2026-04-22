from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import SongForm, UpdateSongForm
from .models import Song
from apps.song_gen_request.models import SongGenRequest
import requests as req
import os

@method_decorator(login_required, name='dispatch')
class LibraryView(ListView):
    def get(self, request):
        pending = SongGenRequest.objects.filter(user=request.user, song=None)
        for song_request in pending:
            if not song_request.task_id:
                continue
            try:
                suno_api_key = os.getenv("SUNO_API_KEY")
                headers = {"Authorization": f"Bearer {suno_api_key}"}
                resp = req.get(
                    f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={song_request.task_id}",
                    headers=headers,
                    timeout=10
                )
                json_data = resp.json()
                if json_data.get("code") == 200 and json_data["data"]["status"].upper() == "SUCCESS":
                    clips = json_data["data"]["response"]["sunoData"]
                    if clips:
                        clip = clips[0]
                        song = Song.objects.create(
                            title=song_request.song_title,
                            duration=int(clip.get("duration") or 0),
                            song_url=clip.get("audioUrl", ""),
                            image_url=clip.get("imageUrl", ""),
                            lyrics=clip.get("prompt", ""),
                            user=song_request.user
                        )
                        song_request.song = song
                        song_request.generation_status = SongGenRequest.Generation_Status.SUCCESS
                        song_request.save()
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
        song = get_object_or_404(Song, pk=song_id)
        song.delete()
        messages.success(request, "Song deleted successfully!")
        return redirect("read_song")
