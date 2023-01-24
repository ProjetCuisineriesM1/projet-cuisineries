# chat/views.py
from django.shortcuts import render,redirect
from datetime import datetime,timedelta
from site_cuisineries.models import Vacation
from site_cuisineries.models import Membre
from site_cuisineries.models import Reunion
from site_cuisineries.models import Conversation
from site_cuisineries.models import Message
def index(request):
    members_list=Membre.objects.all()
    context = {
        'members' : members_list.values("id", "first_name"),
    }
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    start_date = datetime.now() - timedelta(days=30)
    message_list=Message.objects.filter(date__gte=start_date,conversation=room_name)
    context ={
        'message_list' : message_list.values,
        "room_name": room_name,
    }
    return render(request, "chat/room.html", context)


def join(request, room_name):
    
    value=Membre.objects.get(id=room_name)
    if((Conversation.objects.filter(pers1=value,pers2=request.user).exists()) ):
        conv_id=Conversation.objects.get(pers1=value,pers2=request.user)
    elif(Conversation.objects.filter(pers1=request.user,pers2=value).exists()) :
        conv_id=Conversation.objects.get(pers1=request.user,pers2=value)
    else :
        test= Conversation(pers1=value,pers2=request.user)
        test.save()
        conv_id=Conversation.objects.get(pers1=value,pers2=request.user)
    context = {
        'conv_id' : conv_id.id,
    }
    return redirect('/chat/'+str(conv_id.id))
    