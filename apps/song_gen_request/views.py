from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import SongGenRequestForm, UpdateSongGenRequestForm
from .models import SongGenRequest
from apps.song.models import Song
import requests as req
import os

@method_decorator(login_required, name='dispatch')
class CreateSongGenRequestView(CreateView):
    def get(self, request):
        form = SongGenRequestForm()
        return render(request, "create-song-form.html", {"form": form})

    def post(self, request):
        form = SongGenRequestForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["song_title"]
            mood = form.cleaned_data["mood"]
            genre = form.cleaned_data["genre"]
            occasion = form.cleaned_data["occasion"]
            singer_voice_type = form.cleaned_data["singer_voice_type"]
            optional_story = form.cleaned_data["optional_story"]
            instrumental = request.POST.get("instrumental") == "true"
            suno_api_key = os.getenv("SUNO_API_KEY")

            headers = {
                "Authorization": f"Bearer {suno_api_key}",
                "Content-Type": "application/json"
            }
            style_desc = f"{genre}, {mood}"
            if occasion:
                style_desc += f", {occasion}"
            body = {
                "customMode": False,
                "instrumental": instrumental,
                "model": "V4_5ALL",
                "callBackUrl": "https://api.example.com/callback",
                "prompt": f"A {mood} {genre} song for {occasion}. {optional_story}".strip(),
                "style": style_desc,
                "title": title,
            }
            if not instrumental:
                body["vocalGender"] = singer_voice_type

            try:
                resp = req.post("https://api.sunoapi.org/api/v1/generate", json=body, headers=headers, timeout=15)
                json_data = resp.json()
            except Exception:
                messages.error(request, "Could not reach the generation service. Please try again.")
                return render(request, "create-song-form.html", {"form": form})

            if json_data.get("code") == 200:
                task_id = json_data["data"]["taskId"]
                song_request = form.save(commit=False)
                song_request.task_id = task_id
                song_request.user = request.user
                song_request.save()
                messages.success(request, "Song generation started! Check back in a couple of minutes.")
                return redirect("library")
            else:
                messages.error(request, json_data.get("msg", "Generation failed. Please try again."))
                return render(request, "create-song-form.html", {"form": form})
        else:
            messages.error(request, "Please fix the errors below.")
            return render(request, "create-song-form.html", {"form": form})


class ListSongGenRequestView(ListView):
    def get(self, request):
        requests = SongGenRequest.objects.all().order_by('-created_at')
        return render(request, "song_gen_request/read-song-gen-request.html", {"requests": requests})

class UpdateSongGenRequestView(UpdateView):
    def get(self, request, request_id):
        song_gen_request = get_object_or_404(SongGenRequest, pk=request_id)
        form = UpdateSongGenRequestForm(instance=song_gen_request)
        return render(request, "song_gen_request/update-song-gen-request.html", {"form": form, "req": song_gen_request})
    
    def post(self, request, request_id):
        song_gen_request = get_object_or_404(SongGenRequest, pk=request_id)
        form = UpdateSongGenRequestForm(request.POST, instance=song_gen_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Song generation request updated successfully!")
            return redirect("read_song_gen_request")
        else:
            messages.error(request, "Failed to update request. Please check your inputs.")

class DeleteSongGenRequest(DeleteView):
    def get(self, request, request_id):
        return render(request, "song_gen_request/delete-song-gen-request.html")
    
    def post(self, request, request_id):
        song_gen_request = get_object_or_404(SongGenRequest, pk=request_id)
        song_gen_request.delete()
        messages.success(request, "Song generation request deleted successfully!")
        return redirect("read_song_gen_request")

class SongGenStatusView(APIView):
    def get(self, request, taskId):
        suno_api_key = os.getenv("SUNO_API_KEY")
        headers = {"Authorization": f"Bearer {suno_api_key}"}
        
        resp = req.get(f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={taskId}", headers=headers)
        json_data = resp.json()
        code = json_data["code"]
        
        if code == 200:
            if json_data["data"]["status"].upper() == "SUCCESS":
                try:
                    song_request = SongGenRequest.objects.get(task_id=taskId)
                except SongGenRequest.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                if not song_request.song:
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
                
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(json_data, status=status.HTTP_400_BAD_REQUEST)