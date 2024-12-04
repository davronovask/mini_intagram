from django import forms

from users.models import Account
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

image = forms.ImageField(required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['avatar']