from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.translation import ngettext
from import_export.admin import ExportActionMixin

admin.site.unregister(Group)

# Register your models here.
from .models import Membre, Vacation, Inscription, Reunion, Contrepartie, Choix, Attente, Competence

class MembreAdmin(admin.ModelAdmin):
     fields = ('username','first_name', 'last_name','groups','email','telephone', 'cat_sociopro', 'referent', 'competences', 'attentes')
     list_display = ('__str__','role')
     list_filter = ('groups__name',)
     search_fields = ("last_name__icontains", "first_name__icontains", )
     @admin.display(description="Rôle")
     def role(self, obj):
          return obj.groups.values_list('name',flat = True)[0]
admin.site.register(Membre, MembreAdmin)
class VacationAdmin(ExportActionMixin, admin.ModelAdmin):
     list_display = ('nom','date_debut', 'nombre_inscrits', 'complet')
     date_hierarchy = 'date_debut'
     search_fields = ("nom__icontains", )
     @admin.display(description="Nombre d'inscrits")
     def nombre_inscrits(self, obj):
          return str(obj.nb_inscrits())+"/"+str(obj.nb_max_inscrit)
     @admin.display(boolean=True, description="Complet ?")
     def complet(self, obj):
          return obj.nb_inscrits()==obj.nb_max_inscrit
admin.site.register(Vacation,VacationAdmin)
class InscriptionAdmin(admin.ModelAdmin):
     list_display = ('membre', 'vacation', 'participation_valide')
     list_filter = ('vacation','vacation__date_debut')
admin.site.register(Inscription, InscriptionAdmin)
class ReunionAdmin(admin.ModelAdmin):
     list_display = ('membre', 'referent', 'date')
admin.site.register(Reunion, ReunionAdmin)
class ContrepartieAdmin(ExportActionMixin, admin.ModelAdmin):
     list_display = ('nom', 'quantite_dispo')
admin.site.register(Contrepartie, ContrepartieAdmin)

class ChoixAdmin(admin.ModelAdmin):
     list_display = ('membre', 'contrepartie' ,'recupere', 'date')
     list_filter = ('membre', 'contrepartie','recupere',)
     actions = ["mark_recupere"]
     
     @admin.action(description='Marquer comme récupéré')
     def mark_recupere(self, request, queryset):
          updated = queryset.update(recupere=True)
          self.message_user(request, ngettext(
            '%d contrepartie a été marqué comme récupéré.',
            '%d contreparties ont étés marqués comme récupérés.',
            updated,
        ) % updated, messages.SUCCESS)

admin.site.register(Choix, ChoixAdmin)
admin.site.register(Competence)
admin.site.register(Attente)