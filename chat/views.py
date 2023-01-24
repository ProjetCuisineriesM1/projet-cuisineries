# chat/views.py
from django.shortcuts import render

from site_cuisineries.models import Vacation
from site_cuisineries.models import Membre
from site_cuisineries.models import Reunion

def index(request):
    members_list=Membre.objects.all()
    context = {
        'members' : members_list.values("id", "first_name"),
    }
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})