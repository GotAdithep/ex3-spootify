from rest_framework import serializers
from .models import SongGenRequest

class SongGenRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = SongGenRequest
        fields = "__all__"