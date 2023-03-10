
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profil', views.profil, name='profil'),
    path('profil/<int:userid>', views.profil_admin, name='profil admin'),
    path('profil/edit', views.editProfil, name='édition du profil'),
    path('profil/<int:userid>/edit', views.editProfilAdmin, name='édition du profil admin'),
    path('login', views.login, name='Connecter'),
    path('logout', views.logout_user, name='Déconnexion'),
    path('ajax/calendar', views.computeCalendar, name="computeCalendar"),
    path('ajax/newuser', views.ajaxNewUser, name="ajaxNewUser"),
    path('ajax/choixContrepartie', views.ajaxChoixContrepartie, name="ajaxChoixContrepartie"),
    path('contrepartie', views.listeContrepartie),
    path('vacations/<int:vacation>', views.vacation),
    path('reunions/<int:reunion>', views.reunion),
    path("chat/", include("chat.urls")),
    path('profils', views.viewprofile, name='ViewProfile'),
    path("user/add", views.adduser, name="Ajouter un utilisateur"),
    path('myvacation', views.mes_vacations, name='mes vacations'),
    path('mycontreparties', views.mes_contreparties, name='mes contreparties'),
    path('validation', views.validation, name='valdiations'),
    path('askreunion', views.ask, name='demander reunion'),
    path('statistiques', views.statistiques, name='Statistiques'),
    path('ajax/statistiques', views.ajaxStatistiques, name='Statistiques'),
]