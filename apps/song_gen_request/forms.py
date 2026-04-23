from django.forms import ModelForm
from .models import SongGenRequest

class SongGenRequestForm(ModelForm):
    class Meta:
        model = SongGenRequest
        fields = [
            "song_title",
            "mood",
            "genre",
            "occasion",
            "singer_voice_type",
            "optional_story",
        ]
        
class UpdateSongGenRequestForm(ModelForm):
    class Meta:
        model = SongGenRequest
        fields = ["song_title", "task_id", "mood", "genre", "occasion", "singer_voice_type","generation_status", "song"]