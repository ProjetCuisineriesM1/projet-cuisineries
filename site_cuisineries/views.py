from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.db.models import Q

from .models import Vacation
from .models import Membre
from .models import Reunion
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    reunion_list=Reunion.objects.filter(membre_id=request.user.id)
    vacation_list=Vacation.objects
    context = {
        'reunion_list':reunion_list,
        'vacation_list':vacation_list,
    }
    return render(request, 'site_cuisineries/index.html', context)

def profile(request):
    competences_list= Membre.objects.get(email=request.user.email)
    reunion_id_list= Reunion.objects.filter(membre_id=request.user.id)
    context = {
        'competences_list':  competences_list.competences,
        'reunion_id_list':  reunion_id_list,
    }
    return render(request, 'site_cuisineries/profile.html', context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'site_cuisineries/login.html')
    else:
        return render(request, 'site_cuisineries/login.html')

def compute(request):
    vacation_list=list(Vacation.objects.filter(date_debut__year=request.POST.get('annee')).values('date_debut').filter(date_debut__month=request.POST.get('mois')))
    reunion_list=list(Reunion.objects.filter(Q(membre_id=request.user.id) | Q(referent_id=request.user.id)).filter(date__year=request.POST.get('annee')).filter(date__month=request.POST.get('mois')).values('date'))
    return JsonResponse({'vacations': vacation_list, 'reunions': reunion_list})
    
def chat(request):
    person= Membre.objects.get(id=1)
    context = {
        'person': person,
    }
    return render(request, 'site_cuisineries/chat.html', context)
