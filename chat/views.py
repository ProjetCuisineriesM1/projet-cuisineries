# chat/views.py
from django.shortcuts import render,redirect
from datetime import datetime,timedelta
from site_cuisineries.models import Vacation
from site_cuisineries.models import Membre
from site_cuisineries.models import Reunion
from site_cuisineries.models import Conversation
from site_cuisineries.models import Message
from site_cuisineries.models import Inscription
from site_cuisineries.models import MessageGroup
from site_cuisineries.models import ConversationRead1o1, ConversationReadGroup
from site_cuisineries.views import default_context

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
        
    members_list=Membre.objects.all()
    
    inscription_list=Inscription.objects.filter(membre_id=request.user.id)
    vacation_list=Vacation.objects.all()
    context = default_context(request)
    
    context['members']=members_list.values("id","last_name", "first_name")
    context['vacation_list']=vacation_list
    context['inscription_list']= inscription_list
    
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    start_date = datetime.now() - timedelta(days=30)
    message_list=Message.objects.filter(date__gte=start_date,conversation=room_name)
    person=Conversation.objects.get(id=room_name)
    pers1=person.pers1
    pers2=person.pers2
    convRead = ConversationRead1o1.objects.get(conversation=person, membre=request.user)
    convRead.message = message_list.exclude(sender=request.user).last()
    convRead.save()
    
    context = default_context(request)
    context['message_list']= message_list.values
    context["room_name"]= room_name
    context['pers1']= pers1
    context['pers2']= pers2
    


    return render(request, "chat/room.html", context)


def join(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    value=Membre.objects.get(id=room_name)
    if((Conversation.objects.filter(pers1=value,pers2=request.user).exists()) ):
        conv_id=Conversation.objects.get(pers1=value,pers2=request.user)
    elif(Conversation.objects.filter(pers1=request.user,pers2=value).exists()) :
        conv_id=Conversation.objects.get(pers1=request.user,pers2=value)
    else :
        test= Conversation(pers1=value,pers2=request.user)
        test.save()
        ConversationRead1o1(conversation=test,membre=value).save()
        ConversationRead1o1(conversation=test,membre=request.user).save()
        conv_id=Conversation.objects.get(pers1=value,pers2=request.user)
    context = {
        'conv_id' : conv_id.id,
        
        
    }
    return redirect('/chat/'+str(conv_id.id))

def roomGroupe(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    start_date = datetime.now() - timedelta(days=30)
    message_list=MessageGroup.objects.filter(date__gte=start_date,conversation_id=room_name)
    inscription=Inscription.objects.filter(vacation_id=room_name)
    vacation=Vacation.objects.get(id=room_name)
    
    convRead = ConversationReadGroup.objects.get(conversation=vacation, membre=request.user)
    convRead.message = message_list.exclude(sender=request.user).last()
    convRead.save()
    
    context = default_context(request)
    context['message_list']= message_list.values
    context["room_name"]= room_name
    context['inscription']= inscription
    context['vacation']= vacation
    
    return render(request, "chat/roomGroup.html", context)
def join2(request, room_name):
   
    return redirect('/chat/group/'+str(room_name))
    