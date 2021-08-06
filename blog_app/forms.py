from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class Userregister(UserCreationForm):
    email = forms.EmailField(label='Email Address',widget=forms.TextInput(
    attrs={'type': 'email',
           'placeholder': 'E-mail address'}))

    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']



