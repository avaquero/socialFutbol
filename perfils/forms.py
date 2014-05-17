from django import  forms

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
    equip = forms.CharField(max_length=50)
    