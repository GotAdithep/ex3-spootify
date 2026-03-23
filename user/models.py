from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    daily_gen_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "user"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    