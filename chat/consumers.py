import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from site_cuisineries.models import Conversation,ConversationRead1o1,ConversationReadGroup
from site_cuisineries.models import Message,MessageGroup,Vacation
from site_cuisineries.models import Membre
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        self.room_group_name = "chat_%s" % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message = text_data_json["message"]
            
            input_mess=Message(conversation=Conversation.objects.get(id=self.room_name),sender= Membre.objects.get(id=int(text_data_json["sender"])),message=message,date=datetime.now())
            input_mess.save()
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                
                self.room_group_name, {"type": "chat_message", "message": message, "sender":text_data_json["sender"],"sender":text_data_json["sender"], "id":input_mess.id}
            )
        if text_data_json["type"] == "read":
            convRead = ConversationRead1o1.objects.get(conversation=Conversation.objects.get(id=self.room_name),membre=Membre.objects.get(id=int(text_data_json["id"])))
            convRead.message = Message.objects.get(id=int(text_data_json["message"]))
            convRead.save()

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,"sender": sender,"id":event["id"]}))

class ChatConsumer2(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        self.room_group_name = "chat_%s" % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message = text_data_json["message"]
            name=Membre.objects.get(id=int(text_data_json["sender"]))
            input_mess=MessageGroup(conversation=Vacation.objects.get(id=self.room_name),sender= Membre.objects.get(id=int(text_data_json["sender"])),message=message,date=datetime.now())
            input_mess.save()
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": message, "sender":text_data_json["sender"], "id":input_mess.id, "first_name":name.first_name}
            )
        if text_data_json["type"] == "read":
            convRead = ConversationReadGroup.objects.get(conversation=Vacation.objects.get(id=self.room_name),membre=Membre.objects.get(id=int(text_data_json["id"])))
            convRead.message = MessageGroup.objects.get(id=int(text_data_json["message"]))
            convRead.save()

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        name=Membre.objects.get(id=sender)
        # Send message to WebSocket 
        self.send(text_data=json.dumps({"message": message,"sender": sender,"id":event["id"],"first_name": name.first_name +" "+ name.last_name}))