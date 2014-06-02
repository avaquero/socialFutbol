from django.db import models
from perfils.models import Perfil
import datetime
from django.utils import timezone
# Create your models here.

class Publicacio(models.Model):
    usuari = models.ForeignKey(Perfil)
    privat = models.BooleanField()
    dataHora = models.DateTimeField(default=timezone.now)
    imatge = models.FileField(upload_to="imatges", blank=True)
    text = models.TextField()
    url = models.URLField(blank=True)
    
class Comentari(models.Model):
    publicacio = models.ForeignKey(Publicacio)
    usuari = models.ForeignKey(Perfil)
    comentari = models.TextField()
    dataHora = models.DateTimeField(default=timezone.now)
