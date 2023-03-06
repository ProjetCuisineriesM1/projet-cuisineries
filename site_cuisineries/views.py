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
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout, login as auth_login
from django.utils import timezone
from datetime import datetime
import subprocess
import os
from binascii import a2b_base64


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    reunion_list=Reunion.objects.filter(membre_id=request.user.id)
    
    today = datetime.today()
    date_today_b= datetime(today.year,today.month,today.day,0,0,0)
    date_today_e= datetime(today.year,today.month,today.day,23,59,59)
        
    dated = str(timezone.now().strftime("%Y-%m-%d"))
    datef7 = str((timezone.now()+timezone.timedelta(days=7)).strftime("%Y-%m-%d"))
    datef30 = str((timezone.now()+timezone.timedelta(days=30)).strftime("%Y-%m-%d"))
    vacation_list_today=Vacation.objects.filter(date_debut__range=[date_today_b, date_today_e])
    vacation_list_7days=Vacation.objects.filter(date_debut__range=[dated, datef7])
    cat = request.user.competences.all()
    vacation_list_interested_30days=Vacation.objects.filter(date_debut__range=[dated, datef30], categorie__in=cat)

    context = {
        'reunion_list':reunion_list,
        'vacation_list_7days':vacation_list_7days,
        'vacation_list_interested_30days':vacation_list_interested_30days,
        'vacation_list_today':vacation_list_today
    }
    return render(request, 'site_cuisineries/index.html', context)

def profil(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    membre_info= Membre.objects.get(email=request.user.email)
    reunion_id_list= Reunion.objects.filter(membre_id=request.user.id)
    context = {
        'membre_info':  membre_info,
        'competences_list' : membre_info.competences.all(),
        'reunion_id_list':  reunion_id_list,
        'attentes_list' : membre_info.attentes.all()
    }
    return render(request, 'site_cuisineries/profil.html', context)

def profil_admin(request, userid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    #if not request.user.groups.filter(name__in=["Administrateur"]).exists() :
    #    return HttpResponseRedirect('/')
    membre_info= Membre.objects.get(id=userid)
    reunion_id_list= Reunion.objects.filter(membre_id=userid)
    context = {
        'membre_info':  membre_info,
        'competences_list' : membre_info.competences.all(),
        'reunion_id_list':  reunion_id_list,
        'attentes_list' : membre_info.attentes.all()
    }
    return render(request, 'site_cuisineries/profil.html', context)

def adduser(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if not request.user.groups.filter(name__in=["Référent", "Administrateur"]).exists() :
        return HttpResponseRedirect('/')

    referents = Membre.objects.filter(groups__name="Référent")

    context = {
        "referents": referents
    }

    return render(request, 'site_cuisineries/useradd.html', context)

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

def computeCalendar(request):
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

def ajaxNewUser(request):
    reponse = {}
    if not request.user.is_authenticated:
        return JsonResponse({"Erreur": "Vous n'êtes pas autorisés à accéder à cete page !"})
    if not request.user.groups.filter(name__in=["Référent", "Administrateur"]).exists() :
        return JsonResponse({"Erreur": "Vous n'êtes pas autorisés à accéder à cete page !"})
    
    if request.POST.get('step') == "1":
        nUser = Membre.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), first_name=request.POST.get('firstname'), last_name=request.POST.get('lastname'), telephone=request.POST.get('telephone'))
        nUser.set_password(request.POST.get('password'))
        if request.POST.get('role') == "Adhérent":
            nUser.referent = Membre.objects.get(id=int(request.POST.get('referent')))
        nUser.save()

        uGroup = Group.objects.get(name=request.POST.get('role')) 
        uGroup.user_set.add(nUser)
        reponse = {"result":True, "id":nUser.id}

    if request.POST.get('step') == "2":

        pictureFile = request.FILES.get('picture')

        path_to_img = os.path.join("static/profils/", "temporary")

        # Check if today_folder already exists
        if not os.path.exists(path_to_img):
            os.mkdir(path_to_img)

        img_path = os.path.join(path_to_img, request.POST.get("id_user")+"."+pictureFile.name.split(".")[-1])

        # Start writing to the disk
        with open(img_path, 'wb+') as destination:

            if pictureFile.multiple_chunks:  # size is over than 2.5 Mb
                for chunk in pictureFile.chunks():
                    destination.write(chunk)
            else:
                destination.write(pictureFile.read())

        out = subprocess.run("gimp -i -b '(filterImage \"/home/debian/projet-cuisineries/static/profils/temporary/"+(request.POST.get("id_user")+"."+pictureFile.name.split(".")[-1])+"\" )' -b '(gimp-quit 0)'", shell=True)
        print(out)
        reponse = {"result":True, "src":"/"+img_path}

    if request.POST.get('step') == "3":

        pictureFile = a2b_base64(request.POST.get('picture').split(",")[1])

        path_to_img = os.path.join("static/profils/", "temporary")

        # Check if today_folder already exists
        if not os.path.exists(path_to_img):
            os.mkdir(path_to_img)

        img_path = os.path.join(path_to_img, request.POST.get("id_user")+".png")

        # Start writing to the disk
        with open(img_path, 'wb+') as destination:
            destination.write(pictureFile)

        #out = subprocess.run("gimp -i -b '(filterImage \"/home/debian/projet-cuisineries/static/profils/temporary/"+request.POST.get("id_user")+".png"+"\" )' -b '(gimp-quit 0)'", shell=True)
        #print(out)
        reponse = {"result":True, "src":"/"+img_path}

        
    if request.POST.get('step') == "4":

        os.rename("/home/debian/projet-cuisineries/static/profils/temporary/"+request.POST.get("id_user")+".png", "/home/debian/projet-cuisineries/static/profils/"+request.POST.get("id_user")+".png")

        new_user = Membre.objects.get(id=int(request.POST.get("id_user")))
        new_user.photo = "static/profils/"+request.POST.get("id_user")+".png"
        new_user.save()

        reponse = {"result":True}


    return JsonResponse(reponse)
    
def vacation(request, vacation):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    vacation_data=Vacation.objects.get(id=vacation)
    inscrit = Inscription.objects.filter(vacation=vacation_data, membre=request.user).exists()

    membre = Membre.objects.get(id=request.user.id)
    
    context = {
        'vacation_data':vacation_data,
        'inscrit':inscrit
    }

    if request.user.groups.filter(name__in=["Référent", "Administrateur"]).exists() :
        context['liste_inscrits'] = Inscription.objects.filter(vacation=vacation_data).all()
        context['validation'] = vacation_data.date_debut < timezone.now()


    if request.method == 'POST':
        if request.POST['formname'] == "inscription":
            if request.POST['status'] == "0" and vacation_data.nb_inscrits() < vacation_data.nb_max_inscrit:
                Inscription(vacation=vacation_data, membre=request.user).save()
                context["inscrit"] = True
            elif request.POST['status'] == "1":
                Inscription.objects.get(vacation=vacation_data, membre=request.user).delete()
                context["inscrit"] = False
            else:
                context["error_message"] = "Erreur lors de l'inscription"
                return render(request, 'site_cuisineries/vacation.html', context)
        if request.POST['formname'] == "validationPresence":
            if request.POST['valide'] == "1":
                valideUser = Membre.objects.get(id=request.POST['user'])
                inscr = Inscription.objects.get(vacation=vacation_data, membre=valideUser)
                inscr.participation_valide = True
                inscr.save()
            if request.POST['valide'] == "0":
                valideUser = Membre.objects.get(id=request.POST['user'])
                inscr = Inscription.objects.get(vacation=vacation_data, membre=valideUser)
                inscr.participation_valide = False
                inscr.save()
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

def viewprofile(request):
    members_list=Membre.objects.all()
    context = {
        'members' : members_list.values("id", "first_name","last_name"),
    }
    return render(request, 'site_cuisineries/viewprofile.html', context)


def join(request, room_name):
        return HttpResponseRedirect('/profil/'+str(room_name))
    