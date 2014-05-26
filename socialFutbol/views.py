# -*- encoding: utf-8 -*-
from django.shortcuts import render
from perfils.models import Perfil, Solicitud
from xarxa.models import Publicacio, Comentari
from django.db.models import Q
from xarxa.forms import FormNouComentari
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

def home(request):
    if request.user.is_authenticated():
        
        #Formulari per comentar desde inici
        if request.method == 'GET':
            com = FormNouComentari(request.GET)
            if com.is_valid():      
                comentari=com.save(commit=False)
                comentari.publicacio_id = request.GET['publicacio']
                comentari.usuari = request.user.perfil
                comentari.save()
                pagina = reverse('home')
                return HttpResponseRedirect(pagina)
        else:
            com = FormNouComentari()
        

        com.fields['comentari'].widget.attrs['class'] = 'form-control'
        
        yo = request.user.perfil
        amics = Solicitud.objects.filter(
                                         Q(usuariSolicitant_id = yo) | Q(usuariDestinatari_id = yo),
                                         Q(acceptat = True)
                                         )
        publicacions = []
        comentaris = []
        
        for amic in amics:
            if amic.usuariSolicitant_id == yo.id:
                user_act = Perfil.objects.get(usuari = amic.usuariDestinatari_id)
            else:
                user_act = Perfil.objects.get(usuari = amic.usuariSolicitant_id)
                                
            publicacio = Publicacio.objects.filter(usuari_id = user_act).exists()
            if publicacio:
                publicacio = Publicacio.objects.filter(usuari_id = user_act).order_by('-dataHora')
                publicacions.append(publicacio)
                comentari = Comentari.objects.filter(publicacio_id = publicacio).exists()
                if comentari:
                    comentari = Comentari.objects.filter(publicacio_id = publicacio)
                    comentaris.append(comentari)
        
        
        context = {'publicacions':publicacions, 'comentaris':comentaris, 'perfil':yo, 'com':com}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')