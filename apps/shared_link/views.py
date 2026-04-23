import uuid
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from apps.song.models import Song
from .models import SharedLink


@method_decorator(login_required, name='dispatch')
class CreateShareLinkView(View):
    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id, user=request.user)

        existing = SharedLink.objects.filter(
            song=song, expired_date__gt=timezone.now()
        ).first()

        if existing:
            link = existing
        else:
            token = uuid.uuid4().hex
            link = SharedLink.objects.create(
                song=song,
                shared_url=token,
                expired_date=timezone.now() + timedelta(days=7),
            )

        share_url = request.build_absolute_uri(f"/s/{link.shared_url}/")
        return JsonResponse({"url": share_url})


class SharedSongView(View):
    def get(self, request, token):
        link = get_object_or_404(SharedLink, shared_url=token)
        if link.is_expired:
            return render(request, "shared_link/expired.html", status=410)
        return render(request, "shared_link/shared-song.html", {"song": link.song, "link": link})
