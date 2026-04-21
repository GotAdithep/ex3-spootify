from django.forms import ModelForm
from .models import Song

class SongForm(ModelForm):
    class Meta:
        model = Song
        # We exclude 'created_at' because it is auto-generated
        fields = [
            "title", 
            "duration", 
            "user"
        ]

class UpdateSongForm(ModelForm):
    class Meta:
        model = Song
        fields = ["title", "duration", "user"]