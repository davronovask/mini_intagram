from django import forms

from users.models import Account
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio']