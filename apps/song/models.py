from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    song_url = models.URLField(max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="song", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "song"
        
    def __str__(self):
        return f"{self.title}"
        
    