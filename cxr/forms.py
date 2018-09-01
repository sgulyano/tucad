from django import forms

from .models import ChestXray


class ChestXrayForm(forms.ModelForm):
    class Meta:
        model = ChestXray
        fields = ('file', )
