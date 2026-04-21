from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="song", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "song"
        
    def __str__(self):
        return f"{self.title}"
        
    