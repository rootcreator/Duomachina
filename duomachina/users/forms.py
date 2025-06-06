from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'})
        }

class ArtistRegisterForm(UserCreationForm):
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    website = forms.URLField(required=False)
    social_links = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter your social media links (one per line)',
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'bio', 'website', 'social_links', 'avatar'
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_artist = True
        if commit:
            user.save()
        return user 