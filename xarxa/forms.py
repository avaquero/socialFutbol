# -*- encoding: utf-8 -*-
from django import forms
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
        
class BuscaForm(forms.Form):
    busca = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Cerca perfils','autocomplete':'off'}))