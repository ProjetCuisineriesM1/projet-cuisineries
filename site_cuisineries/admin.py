from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.translation import ngettext
from import_export.admin import ExportActionMixin

admin.site.unregister(Group)

# Register your models here.
from .models import Membre, Vacation, Inscription, Reunion, Contrepartie, Choix, Attente, Competence

class MembreAdmin(admin.ModelAdmin):
     #: Ensemble des valeurs à afficher dans le panneau d'administration
     fields = ('username','first_name', 'last_name','groups','email','telephone', 'cat_sociopro', 'referent', 'competences', 'attentes')
     
     #: Eléments à afficher dans le tableau récapitulatif des utilisateurs
     list_display = ('__str__','role')

     #: Catégories de filtre
     list_filter = ('groups__name',)

     #: Eléments servant à la recherche de données
     search_fields = ("last_name__icontains", "first_name__icontains", )

     @admin.display(description="Rôle")
     def role(self, obj):
          """Renvoie le nom du groupe auquel l'utilisateur appartient."""
          if obj.groups.count() > 0:
               return obj.groups.values_list('name',flat = True)[0]
          else:
               return "Aucun rôle"
admin.site.register(Membre, MembreAdmin)

class VacationAdmin(ExportActionMixin, admin.ModelAdmin):
     #: Eléments à afficher dans le tableau récapitulatif des vacations
     list_display = ('nom','date_debut', 'nombre_inscrits', 'complet')
     
     #: Tri par défaut des vacations
     date_hierarchy = 'date_debut'
     
     #: Eléments servant à la recherche de données
     search_fields = ("nom__icontains", )

     @admin.display(description="Nombre d'inscrits")
     def nombre_inscrits(self, obj):
          """Renvoie le nombre de membre inscrits sur le nombre de places disponibles
          
          :rtype: str
          """
          return str(obj.nb_inscrits())+"/"+str(obj.nb_max_inscrit)
     @admin.display(boolean=True, description="Complet ?")
     def complet(self, obj):
          """Indique si la vacation est complète ou non."""
          return obj.nb_inscrits()==obj.nb_max_inscrit
admin.site.register(Vacation,VacationAdmin)

class InscriptionAdmin(ExportActionMixin, admin.ModelAdmin):
     #: Eléments à afficher dans le tableau récapitulatif des inscriptions
     list_display = ('membre', 'vacation', 'participation_valide')
     
     #: Catégories de filtre
     list_filter = ('vacation','vacation__date_debut', 'participation_valide')
admin.site.register(Inscription, InscriptionAdmin)

class ReunionAdmin(admin.ModelAdmin):
     #: Eléments à afficher dans le tableau récapitulatif des réunions
     list_display = ('membre', 'referent', 'date')

     def get_queryset(self, request):
          """Autorise l'affichage des réunions seulement aux référents participants à la réunion.
          Les administrateurs ont la visibilité sur toutes les réunions."""
          if request.user.groups.filter(name="Administrateur").exists():
               return super().get_queryset(request)
          else:
               return super().get_queryset(request).filter(referent=request.user)
admin.site.register(Reunion, ReunionAdmin)

class ContrepartieAdmin(ExportActionMixin, admin.ModelAdmin):
     #: Eléments à afficher dans le tableau récapitulatif des contreparties
     list_display = ('nom', 'quantite_dispo')
admin.site.register(Contrepartie, ContrepartieAdmin)

class ChoixAdmin(admin.ModelAdmin):
     #: Eléments à afficher dans le tableau récapitulatif des choix
     list_display = ('membre', 'contrepartie' ,'recupere', 'date')
     
     #: Catégories de filtre
     list_filter = ('membre', 'contrepartie','recupere',)
     
     #: Actions exécutables dans le panneau d'administration
     actions = ["mark_recupere"]
     
     @admin.action(description='Marquer comme récupéré')
     def mark_recupere(self, request, queryset):
          """Modifie les choix sélectionnés afin d'indiquer qu'ils ont étés récupérés
          """
          updated = queryset.update(recupere=True)
          self.message_user(request, ngettext(
            '%d contrepartie a été marqué comme récupéré.',
            '%d contreparties ont étés marqués comme récupérés.',
            updated,
        ) % updated, messages.SUCCESS)

admin.site.register(Choix, ChoixAdmin)
admin.site.register(Competence)
admin.site.register(Attente)