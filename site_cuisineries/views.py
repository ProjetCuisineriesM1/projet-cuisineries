from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Vacation
from .models import Membre

from django.contrib.auth.models import User

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    next_vacations_list = Vacation.objects.order_by('-date_debut')[:5]
    context = {
        'next_vacations_list': next_vacations_list,
    }
    return render(request, 'site_cuisineries/index.html', context)

def profile(request):
    competences_list= Membre.objects.get(email=request.user.email)
    context = {
        'competences_list':  competences_list.competences,
    }
    return render(request, 'site_cuisineries/profile.html', context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        context = {
        }
        return render(request, 'site_cuisineries/login.html', context)
