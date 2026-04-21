from django.db import models

# Create your models here.
class SharedLink(models.Model):
    shared_url = models.CharField(max_length=100)
    expired_date = models.DateTimeField()
    song = models.ForeignKey("song.Song", on_delete=models.CASCADE, related_name="shared_link")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "shared_link"
        
    def __str__(self):
        return f"{self.shared_url} {self.expired_date}"