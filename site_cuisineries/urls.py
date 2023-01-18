
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name='Connecter'),
    path('ajax/calendar', views.compute, name="compute"),
    path("chat/", include("chat.urls")),
]