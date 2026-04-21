from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import SongGenRequestForm, UpdateSongGenRequestForm
from .models import SongGenRequest
from .serailizer import SongGenRequestSerializers
import requests as req
import os

class CreateSongGenRequestView(CreateView):
    def get(self, request):
        form = SongGenRequestForm()
        return render(request, "create-song-form.html", {"form": form})
    
    def post(self, request):
        form = SongGenRequestForm(request.POST)
        if form.is_valid():
            # Suno API Call
            title = form.cleaned_data["song_title"]
            mood = form.cleaned_data["mood"]
            genre = form.cleaned_data["genre"]
            occasion = form.cleaned_data["occasion"]
            singer_voice_type = form.cleaned_data["singer_voice_type"]
            optional_story = form.cleaned_data["optional_story"]
            suno_api_key = os.getenv("SUNO_API_KEY")
            
            headers = {
                "Authorization": f"Bearer {suno_api_key}",
                "Content-Type": "application/json"
            }

            body = {
                "customMode": True,
                "instrumental": False,
                "model": "V4_5ALL",
                "callBackUrl": "https://api.example.com/callback",
                "prompt": f"mood={mood}  occasion={occasion}  optional_story={optional_story}",
                "style": genre,
                "title": title,
                "vocalGender": singer_voice_type
            }

            resp = req.post("https://api.sunoapi.org/api/v1/generate", json=body, headers=headers)
            json = resp.json()
            code = json["code"]
            task_id = json["data"]["taskId"]
            if code == 200:
                song_request = form.save(commit=False) 
                song_request.task_id = task_id
                song_request.save()
                messages.success(request, "Song generation request created successfully!")
                return redirect("create-song-form") 
            else:
                messages.error(request, "API falied")
                return redirect("create-song-form") 
            
            
        else:
            print(form.errors)
            messages.error(request, "Failed to create request. Please check your inputs.")
            return redirect("create-song-form")

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
        headers = {
            "Authorization": f"Bearer {suno_api_key}"
        }
        resp = req.get(f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={taskId}",headers=headers)
        json = resp.json()
        code = json["code"]
        if code == 200:
            if json["data"]["status"] == "SUCCESS":
                try:
                    song_request = SongGenRequest.objects.get(task_id = taskId)
                except SongGenRequest.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
                serializer = SongGenRequestSerializers(song_request, data={"generation_status": SongGenRequest.Generation_Status.SUCCESS}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                
            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
            
    
        
    
    