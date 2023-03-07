from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.timezone import now
import math
# Create your models here.

class Competence(models.Model):
    nom = models.CharField(max_length=200, null=False, primary_key=True)
    def __str__(self):
        return self.nom

class Attente(models.Model):
    nom = models.CharField(max_length=200, null=False, primary_key=True)
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
    categorie = models.ManyToManyField(Competence)
    def __str__(self):
        return self.nom+" ("+self.date_debut.strftime("%d/%m/%Y")+")"

    def nb_inscrits(self):
        return Inscription.objects.filter(vacation=self.id).count()

    def credits(self):
        return math.ceil((self.date_fin-self.date_debut).total_seconds()/3600)
    def inscrits(self):
        return Inscription.objects.filter(vacation=self.id).values_list('membre')

class Contrepartie(models.Model):
    nom = models.CharField(max_length=100)
    details = models.TextField(default="")
    credits_requis = models.IntegerField(default=0, null=True)
    quantite_dispo = models.IntegerField(default=0, null=True)
    attente = models.ManyToManyField(Attente)
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
    recupere = models.BooleanField(default=False, verbose_name="récupéré ?")
    date = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return str(self.membre)+" a choisi la contrepartie : "+self.contrepartie.nom
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['contrepartie', 'membre', 'date'], name='unique_contrepartie_mail_combination'
            )
        ]
        verbose_name_plural = "Choix"
class Conversation(models.Model):
    pers1=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name='pers1')
    pers2=models.ForeignKey(Membre, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pers1)+" "+str(self.pers2)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender=models.ForeignKey(Membre, null=True, on_delete=models.SET_NULL)
    message = models.TextField(null=True)
    date = models.DateTimeField()
    def __str__(self):
        return str(self.conversation)+" "+str(self.date)

class MessageGroup(models.Model):
    conversation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    sender=models.ForeignKey(Membre, null=True, on_delete=models.SET_NULL)
    message = models.TextField(null=True)
    date = models.DateTimeField()
    def __str__(self):
        return str(self.conversation)+" "+str(self.date)

class ConversationRead1o1(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, null=True, on_delete=models.SET_NULL)
    def is_new_message(self):
        last_message = Message.objects.filter(conversation=self.conversation).exclude(sender=self.membre).last()
        if last_message.id is not self.message.id:
            return True
        return False
    def nb_not_read(self):
        return Message.objects.filter(conversation=self.conversation, id__gt=self.message.id).exclude(sender=self.membre).count()

class ConversationReadGroup(models.Model):
    conversation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    message = models.ForeignKey(MessageGroup, null=True, on_delete=models.SET_NULL)
    def is_new_message(self):
        last_message = MessageGroup.objects.filter(conversation=self.conversation).exclude(sender=self.membre).last()
        if last_message.id is not self.message.id:
            return True
        return False
    def nb_not_read(self):
        return MessageGroup.objects.filter(conversation=self.conversation, id__gt=self.message.id).exclude(sender=self.membre).count()

