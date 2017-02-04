# -*- coding: utf-8 -*-
from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget())
    class Meta:
        model = Post
        fields = ('title', 'text',)