from django.forms import ModelForm
from .models import UserProfile, User


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'friends']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
