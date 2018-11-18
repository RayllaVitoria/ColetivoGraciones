from .models import Post
from django import forms


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'capa', 'text']


class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'capa', 'text', 'published_date']        