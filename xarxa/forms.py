from django.forms import ModelForm
from django.db import models
from xarxa.models import Publicacio, Comentari

class FormNovaPublicacio(ModelForm):
    class Meta:
        model = Publicacio
        fields = ['text','imatge','privat']

class FormNouComentari(ModelForm):
    class Meta:
        model = Comentari
        fields = ['comentari']