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
from .factory import get_generator_strategy
from .utils import create_song_from_clips


@method_decorator(login_required, name='dispatch')
class CreateSongGenRequestView(CreateView):
    def get(self, request):
        form = SongGenRequestForm()
        return render(request, "create-song-form.html", {"form": form})

    def post(self, request):
        form = SongGenRequestForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Please fix the errors below.")
            return render(request, "create-song-form.html", {"form": form})

        request_data = {
            "title": form.cleaned_data["song_title"],
            "mood": form.cleaned_data["mood"],
            "genre": form.cleaned_data["genre"],
            "occasion": form.cleaned_data["occasion"],
            "singer_voice_type": form.cleaned_data["singer_voice_type"],
            "optional_story": form.cleaned_data["optional_story"],
            "instrumental": request.POST.get("instrumental") == "true",
        }

        try:
            strategy = get_generator_strategy()
            result = strategy.generate(request_data)
        except Exception as e:
            messages.error(request, f"Generation failed: {e}")
            return render(request, "create-song-form.html", {"form": form})

        song_request = form.save(commit=False)
        song_request.task_id = result["task_id"]
        song_request.user = request.user
        song_request.save()

        if result["status"] == "SUCCESS" and result.get("clips"):
            create_song_from_clips(song_request, result["clips"])

        messages.success(request, "Song generation started! Check back in a couple of minutes.")
        return redirect("library")


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
        try:
            strategy = get_generator_strategy()
            result = strategy.get_status(taskId)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if result["status"] == "SUCCESS":
            try:
                song_request = SongGenRequest.objects.get(task_id=taskId)
            except SongGenRequest.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if not song_request.song and result.get("clips"):
                create_song_from_clips(song_request, result["clips"])

        return Response(result, status=status.HTTP_200_OK)
