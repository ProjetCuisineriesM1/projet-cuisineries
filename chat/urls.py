# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("group/<str:room_name>/", views.roomGroupe, name="room"),
    path("join/<int:room_name>/", views.join, name="join"),
]