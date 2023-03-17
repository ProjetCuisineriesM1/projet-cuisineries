from .models import Membre
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def populate_models(sender, **kwargs):
    
    adherent, created = Group.objects.get_or_create(name='Adhérent')
    referent, created = Group.objects.get_or_create(name='Référent')
    administrateur, created = Group.objects.get_or_create(name='Administrateur')

    permission = Permission.objects.get(codename="add_attente")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_attente")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_attente")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_attente")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="add_choix")
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_choix")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_choix")
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_choix")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="add_competence")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_competence")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_competence")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_competence")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="add_contrepartie")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_contrepartie")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_contrepartie")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_contrepartie")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="add_inscription")
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_inscription")
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_inscription")
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_inscription")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="add_reunion")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_reunion")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_reunion")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_reunion")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="add_vacation")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="change_vacation")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_vacation")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_vacation")
    referent.permissions.add(permission)
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="delete_membre")
    administrateur.permissions.add(permission)

    permission = Permission.objects.get(codename="view_membre")
    administrateur.permissions.add(permission)
    