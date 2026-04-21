from django.forms import ModelForm
from .models import SharedLink

class SharedLinkForm(ModelForm):
    class Meta:
        model = SharedLink
        # We exclude 'created_at' because it is auto-generated
        fields = [
            "shared_url", 
            "expired_date", 
            "song"
        ]
        
class UpdateSharedLinkForm(ModelForm):
    class Meta:
        model = SharedLink
        fields = ["shared_url", "expired_date", "song"]