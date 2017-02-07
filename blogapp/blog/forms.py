# -*- coding: utf-8 -*-
from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
#from charsleft_widget.widgets import CharsLeftInput
#from charsleft_widget import CharsLeftArea


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget(show_preview=False), label='')
    #crypt = forms.NullBooleanField(label="Cifrar", initial=False)

    class Meta:
        model = Post
        fields = ('title', 'text', 'crypt', 'key', 'rekey',)
        labels = {'title': '', 'key': 'Password', 'rekey': 'Repite password', }
        widgets = {
        'key': forms.PasswordInput(),
        'rekey': forms.PasswordInput(), }

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        crypt = cleaned_data.get('crypt')
        if crypt is True:
            password = cleaned_data.get('key')
            password_confirm = cleaned_data.get('rekey')
            if password and password_confirm:
                if password != password_confirm:
                    raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data


class KeyCheckForm(forms.Form):
    passw = forms.CharField(label='Contraseña', widget=forms.PasswordInput())