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
    
    def __unicode__(self):
        return self.usuari.username
    
class Solicitud(models.Model):
    usuariSolicitant = models.ForeignKey(Perfil, related_name='usuariSolicitant')
    usuariDestinatari = models.ForeignKey(Perfil, related_name='usuariDestinatari')
    acceptat = models.BooleanField()
    dataAcceptacio = models.DateField(blank=True)
    dataSolicitud = models.DateField(blank=True)