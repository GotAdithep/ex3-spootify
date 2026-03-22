from django.db import models

# Create your models here.
class SongGenRequest(models.Model):
    class Moodchoices(models.TextChoices):
        HAPPY = "happy", "happy"
        ENERGATIC = "energatic", "energatic"
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
        
    song_title = models.CharField(max_length=50)
    mood = models.CharField(max_length=10, choices=Moodchoices.choices,default=Moodchoices.HAPPY)
    genre = models.CharField(max_length=10, choices=Genrechoices.choices,default=Genrechoices.POP)
    occasion = models.CharField(max_length=50)
    singer_voice_type = models.CharField(max_length=50)
    optional_story = models.CharField(max_length=150, null=True, blank=True)
    song = models.OneToOneField("song.Song", on_delete=models.CASCADE, related_name="song_gen_request", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "song_gen_request"
        
    def __str__(self):
        return f"{self.song_title} {self.mood}"