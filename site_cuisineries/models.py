from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Membre(AbstractUser):
    photo = models.FileField(null=True, upload_to='static/profils/', max_length=500)
    attentes = models.TextField(null=True)
    cat_sociopro = models.IntegerField(default=0)
    telephone = models.CharField(max_length=10, null=True)
    nb_heures = models.FloatField(default=0, null=True)
    credits = models.IntegerField(default=0, null=True)
    competences = models.JSONField(null=True)
    referent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    pass
    def __str__(self):
        return self.first_name+" "+self.last_name

class Vacation(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nom = models.CharField(max_length=100)
    nb_max_inscrit = models.FloatField(default=0, null=True)
    def __str__(self):
        return self.nom+" ("+self.date_debut.strftime("%d/%m/%Y")+")"

class Contrepartie(models.Model):
    nom = models.CharField(max_length=100)
    credits_requit = models.IntegerField(default=0, null=True)
    quantite_dispo = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.nom+" ("+str(self.quantite_dispo)+")"

class Reunion(models.Model):
    date = models.DateTimeField()
    referent = models.ForeignKey(Membre, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="membres")
    def __str__(self):
        return "Réunion entre "+str(self.referent)+" et "+str(self.membre)+" ("+self.date.strftime("%d/%m/%Y")+")"

class Inscription(models.Model):
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.membre)+" est inscrit à "+str(self.vacation)

class Choix(models.Model):
    contrepartie = models.ForeignKey(Contrepartie, on_delete=models.PROTECT)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.membre)+" a choisit "+self.contrepartie.nom
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['contrepartie', 'membre'], name='unique_contrepartie_mail_combination'
            )
        ]
        verbose_name_plural = "Choix"