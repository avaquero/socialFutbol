from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuari = models.OneToOneField(User)
    nom = models.CharField(max_length=30)
    cognoms = models.CharField(max_length=30)
    dataNaix = models.DateField()
    equip = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.usuari.username
    
class Amic(models.Model):
    usu1 = models.ForeignKey(Perfil, related_name='usuari1')
    usu2 = models.ForeignKey(Perfil, related_name='usuari2')