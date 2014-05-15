from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuari = models.OneToOneField(User)
    nom = models.CharField(max_length=30)
    cognoms = models.CharField(max_length=30)
    dataNaix = models.DateField()
    equip = models.CharField(max_length=30)
    imatgePerfil = models.FileField(upload_to="imatges", blank=True)
    #nouAmic = models.ManyToManyField("self", blank=True)
    
    def __unicode__(self):
        return self.usuari.username
    
class Amic(models.Model):
    usuari = models.ForeignKey(Perfil, related_name='usuariJo')
    usuariAmic = models.ForeignKey(Perfil, related_name='usuariAmic')
    acceptat = models.BooleanField()
    dataAcceptacio = models.DateField(blank=True)