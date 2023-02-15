from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Competence(models.Model):
    nom = models.CharField(max_length=200, null=False, primary_key=True)
    def __str__(self):
        return self.nom

class Attente(models.Model):
    nom = models.CharField(max_length=200, null=False)
    def __str__(self):
        return self.nom

        
class Membre(AbstractUser):
    photo = models.FileField(null=True, upload_to='static/profils/', max_length=500)
    cat_sociopro = models.IntegerField(default=0)
    telephone = models.CharField(max_length=10, null=True)
    nb_heures = models.FloatField(default=0, null=True)
    credits = models.IntegerField(default=0, null=True)
    competences = models.ManyToManyField(Competence)
    attentes = models.ManyToManyField(Attente)
    referent = models.ForeignKey('self', blank=True, on_delete=models.PROTECT, null=True, limit_choices_to= models.Q( groups__name = 'Référent'))
    pass
    def __str__(self):
        return self.first_name+" "+self.last_name

class Vacation(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True)
    nb_max_inscrit = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.nom+" ("+self.date_debut.strftime("%d/%m/%Y")+")"

    def nb_inscrits(self):
        return Inscription.objects.filter(vacation=self.id).count()

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
    contenu = models.TextField(null=True, blank=True)
    def __str__(self):
        return "Réunion entre "+str(self.referent)+" et "+str(self.membre)

class Inscription(models.Model):
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    participation_valide = models.BooleanField(null=True)
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
class Conversation(models.Model):
    pers1=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name='pers1')
    pers2=models.ForeignKey(Membre, on_delete=models.CASCADE)
    def __str__(self):
        return self.pers1+" "+self.pers2

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender=models.ForeignKey(Membre, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    date = models.DateTimeField()
    def __str__(self):
        return self.conversation+" "+self.date

