from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core import serializers

from .models import Vacation
from .models import Membre
from .models import Reunion
from .models import Inscription
from .models import Attente
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login

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

def profil(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    membre_info= Membre.objects.get(email=request.user.email)
    attentes_list = Attente.objects.filter(membre_id=request.user.id)
    reunion_id_list= Reunion.objects.filter(membre_id=request.user.id)
    context = {
        'membre_info':  membre_info,
        'competences_list' : membre_info.competences.all(),
        'reunion_id_list':  reunion_id_list,
        'attentes_list' : attentes_list
    }
    return render(request, 'site_cuisineries/profil.html', context)

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

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/login')

def compute(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    reponse = {}
    if request.POST.get('requete') == "mois":
        vacation_list=list(Vacation.objects.filter(date_debut__year=request.POST.get('annee')).values('date_debut').filter(date_debut__month=request.POST.get('mois')))
        reunion_list=list(Reunion.objects.filter(Q(membre_id=request.user.id) | Q(referent_id=request.user.id)).filter(date__year=request.POST.get('annee')).filter(date__month=request.POST.get('mois')).values('date'))
        reponse = {'vacations': vacation_list, 'reunions': reunion_list}
    if request.POST.get('requete') == "jour":
        vacation_list=list(Vacation.objects.filter(date_debut__year=request.POST.get('annee')).filter(date_debut__month=request.POST.get('mois')).filter(date_debut__day=request.POST.get('jour')).values("id","date_debut", "date_fin", "nom"))
        reunion_list=list(Reunion.objects.filter(Q(membre_id=request.user.id) | Q(referent_id=request.user.id)).filter(date__year=request.POST.get('annee')).filter(date__month=request.POST.get('mois')).filter(date__day=request.POST.get('jour')).values("id","date", "referent", "membre"))
        for i in reunion_list:
            i["membre"] = list(Membre.objects.filter(id=i["membre"]).values("first_name", "last_name"))[0]
            i["referent"] = list(Membre.objects.filter(id=i["referent"]).values("first_name", "last_name"))[0]
        reponse = {'vacations': vacation_list, 'reunions': reunion_list}
    return JsonResponse(reponse)
    
def vacation(request, vacation):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    vacation_data=Vacation.objects.get(id=vacation)
    inscrit = Inscription.objects.filter(vacation=vacation_data, membre=request.user).exists()
    
    context = {
        'vacation_data':vacation_data,
        'inscrit':inscrit
    }
    if request.method == 'POST':
        if request.POST['status'] == "0" and vacation_data.nb_inscrits() < vacation_data.nb_max_inscrit:
            Inscription(vacation=vacation_data, membre=request.user).save()
            context["inscrit"] = True
        elif request.POST['status'] == "1":
            Inscription.objects.get(vacation=vacation_data, membre=request.user).delete()
            context["inscrit"] = False
        else:
            context["error_message"] = "Erreur lors de l'inscription"
            return render(request, 'site_cuisineries/vacation.html', context)
    context["vacation_data"] = Vacation.objects.get(id=vacation)
    return render(request, 'site_cuisineries/vacation.html', context)    


def reunion(request, reunion):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    reunion_data=Reunion.objects.get(id=reunion)
    
    context = {
        'reunion_data':reunion_data
    }
    
    return render(request, 'site_cuisineries/reunion.html', context)    

