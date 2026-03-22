from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "last_name", "daily_gen_count", "password"]

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "last_name", "daily_gen_count"]