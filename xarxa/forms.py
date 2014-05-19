from django.forms import ModelForm
from django.db import models
from xarxa.models import Publicacio

class FormNovaPublicacio(ModelForm):
    class Meta:
        model = Publicacio
        fields = ['text','imatge','privat']