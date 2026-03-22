from django.db import models

# Create your models here.
class Song(models.Model):
    class Generation_Status(models.TextChoices):
        SUCCESS = "success", "success"
        FAILED = "failed", "failed"
        PENDING = "pending", "pending"
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    generation_status = models.CharField(max_length=7,choices=Generation_Status.choices,default=Generation_Status.PENDING)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="song", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "song"
        
    def __str__(self):
        return f"{self.title}"
        
    