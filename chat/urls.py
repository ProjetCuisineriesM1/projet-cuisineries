# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("group/<str:room_name>/", views.roomGroupe, name="room"),
    path("join/<int:room_name>/", views.join, name="join"),
    path("join2/<int:room_name>/", views.join2, name="join2"),
]