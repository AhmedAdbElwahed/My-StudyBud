from django import forms

from . import models


class RoomForm(forms.ModelForm):

    class Meta:
        model = models.Room
        fields = "__all__"
        exclude = ['host', 'participants']
        # widgets = {
        #     "host": forms.Select(attrs= {'class': 'form-select'}),
        #     "topic": forms.Select(attrs= {'class': 'form-select'}),
        #     "name": forms.TextInput(attrs= {'class': 'form-control'}),
        #     "description": forms.Textarea(attrs= {'class': 'form-control'}),
        # }
