# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponseRedirect

# Create your views here.
def generarPerfil(request):
    return render(request, 'tu.html')