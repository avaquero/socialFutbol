from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuari = models.OneToOneField(User)
    nom = models.CharField(max_length=30)
    cognoms = models.CharField(max_length=30)
    dataNaix = models.DateField()
    equip = models.CharField(max_length=30)
    
class Amic(models.Model):
    usu1 = models.ForeignKey(Perfil, related_name='usuari1')
    usu2 = models.ForeignKey(Perfil, related_name='usuari2')
    
class Publicacio(models.Model):
    usuari = models.ForeignKey(Perfil)
    privat = models.BooleanField()
    dataHora = models.DateTimeField()
    urlImatge = models.TextField()
    text = models.TextField()
    
class Comentari(models.Model):
    publicacio = models.ForeignKey(Publicacio)
    usuari = models.ForeignKey(Perfil)
    comentari = models.TextField()
    dataHora = models.DateTimeField()
