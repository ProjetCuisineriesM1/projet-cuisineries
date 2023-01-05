from django.contrib import admin

# Register your models here.
from .models import Membre, Vacation, Inscription, Reunion, Contrepartie, Choix


admin.site.register(Membre)
admin.site.register(Vacation)
admin.site.register(Inscription)
admin.site.register(Reunion)
class ContrepartieAdmin(admin.ModelAdmin):
     list_display = ('nom', 'quantite_dispo')
admin.site.register(Contrepartie, ContrepartieAdmin)
admin.site.register(Choix)