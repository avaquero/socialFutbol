# -*- encoding: utf-8 -*-
from django.forms import ModelForm
from django import  forms
from perfils.models import Perfil

class formulariLogin(forms.Form):
    usuari = forms.CharField(max_length=100)
    contrasenya = forms.CharField(max_length=100, widget=forms.PasswordInput())

class formulariUsuari(forms.Form):
    usuari = forms.CharField(max_length=100)
    
class formulariRegistrarse(forms.Form):
    nick = forms.CharField(max_length=30)
    contrasenya = forms.CharField(max_length=100, widget=forms.PasswordInput())
    nom = forms.CharField(max_length=50)
    cognoms = forms.CharField(max_length=50)
    dataNaix = forms.DateField()

class formulariModificar(ModelForm):
    class Meta:
        model = Perfil
        fields= ['nom','cognoms', 'dataNaix', 'equip', 'imatgePerfil']
        
class formulariEditarContrasenya(forms.Form):
    antiga = forms.CharField(max_length=100, widget=forms.PasswordInput() )
    nova = forms.CharField(max_length=100, widget=forms.PasswordInput() )
    novaComprova = forms.CharField(max_length=100, widget=forms.PasswordInput() )