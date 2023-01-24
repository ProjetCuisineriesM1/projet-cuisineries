from django.contrib import admin

# Register your models here.
from .models import Membre, Vacation, Inscription, Reunion, Contrepartie, Choix


admin.site.register(Membre)
class VacationAdmin(admin.ModelAdmin):
     list_display = ('nom','date_debut', 'nombre_inscrits', 'complet')
     date_hierarchy = 'date_debut'
     @admin.display(description="Nombre d'inscrits")
     def nombre_inscrits(self, obj):
          return str(obj.nb_inscrits())+"/"+str(obj.nb_max_inscrit)
     @admin.display(boolean=True, description="Complet ?")
     def complet(self, obj):
          return obj.nb_inscrits()==obj.nb_max_inscrit
admin.site.register(Vacation,VacationAdmin)
admin.site.register(Inscription)
admin.site.register(Reunion)
class ContrepartieAdmin(admin.ModelAdmin):
     list_display = ('nom', 'quantite_dispo')
admin.site.register(Contrepartie, ContrepartieAdmin)
admin.site.register(Choix)