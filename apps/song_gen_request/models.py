from django.db import models

# Create your models here.
class SongGenRequest(models.Model):
    class Moodchoices(models.TextChoices):
        HAPPY = "happy", "happy"
        ENERGETIC = "energetic", "energetic"
        SAD = "sad", "sad"
        DEPRESSION = "depression", "depression"
        CALM = "calm", "calm"
        
    class Genrechoices(models.TextChoices):
        POP = "pop", "pop"
        ROCK = "rock", "rock"
        JAZZ = "jazz", "jazz"
        CLASSICAL = "classical", "classical"
        ELECTRONIC = "electronic", "electronic"
        HIPHOP = "hiphop", "hiphop"
        COUNTRY = "country", "country"
        METAL = "metal", "metal"
        
    class Generation_Status(models.TextChoices):
        SUCCESS = "success", "success"
        FAILED = "failed", "failed"
        PENDING = "pending", "pending"
        
    song_title = models.CharField(max_length=50)
    task_id = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="song_gen_requests")
    mood = models.CharField(max_length=10, choices=Moodchoices.choices,default=Moodchoices.HAPPY)
    genre = models.CharField(max_length=10, choices=Genrechoices.choices,default=Genrechoices.POP)
    occasion = models.CharField(max_length=50)
    singer_voice_type = models.CharField(max_length=50)
    optional_story = models.CharField(max_length=150, null=True, blank=True)
    generation_status = models.CharField(max_length=7,choices=Generation_Status.choices, default=Generation_Status.PENDING)
    song = models.OneToOneField("song.Song", on_delete=models.CASCADE, related_name="song_gen_request", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "song_gen_request"
        
    def __str__(self):
        return f"{self.song_title} {self.mood}"