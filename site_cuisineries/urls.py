
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profil', views.profil, name='profil'),
    path('login', views.login, name='Connecter'),
    path('logout', views.logout_user, name='Déconnexion'),
    path('ajax/calendar', views.compute, name="compute"),
    path('vacations/<int:vacation>', views.vacation),
    path('reunions/<int:reunion>', views.reunion),
    path("chat/", include("chat.urls")),
]