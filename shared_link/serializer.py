from rest_framework import serializers
from .models import SharedLink

class Share_linkSerializers(serializers.ModelSerializer):
    class Meta:
        model = SharedLink
        fields = "__all__"