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
    CAT_SOCIOPROFESSIONNEL = [
        ('10', 'Agriculteurs'),
        ('21', 'Artisans'),
        ('22', 'Commerçants et assimilés'),
        ('23', 'Chefs d\'entreprise de plus de 10 personnes'),
        ('31', 'Professions libérales'),
        ('33', 'Cadres de la fonction publique'),
        ('34', 'Professeurs et professions scientifiques'),
        ('35', 'Professions de l\'information, de l\'art et des spectacles'),
        ('37', 'Cadres administratifs et commerciaux'),
        ('38', 'Cadres techniques d\'entreprise'),
        ('42', 'Professions de l\'enseignement primaire et professionnel'),
        ('43', 'Intermédiaires de la santé et du travail social'),
        ('44', 'Religieux'),
        ('45', 'Intermédiaires de la fonction publique'),
        ('46', 'Intermédiaires des entreprises'),
        ('47', 'Techniciens'),
        ('48', 'Agents de maîtrise de production'),
        ('52', 'Employés de la fonction publique'),
        ('53', 'Policiers, militaires et agents de sécurité privée'),
        ('54', 'Employés administratifs d\'entreprise'),
        ('55', 'Employés de commerce'),
        ('56', 'Personnels des services aux particuliers'),
        ('62', 'Ouvriers qualifiés de type industriel'),
        ('63', 'Ouvriers qualifiés de type artisanal'),
        ('64', 'Conducteurs du transport'),
        ('65', 'Conducteurs d\'engins et magasiniers'),
        ('67', 'Ouvriers peu qualifiés de type industriel'),
        ('68', 'Ouvriers peu qualifiés de type artisanal'),
        ('69', 'Ouvriers agricoles'),
    ]

    photo = models.FileField(null=True, upload_to='static/profils/', max_length=500)
    cat_sociopro = models.CharField(null=True, choices=CAT_SOCIOPROFESSIONNEL, max_length=2)
    telephone = models.CharField(max_length=10, null=True)
    nb_heures = models.FloatField(default=0, null=True)
    credits = models.IntegerField(default=0, null=True)
    competences = models.ManyToManyField(Competence)
    attentes = models.ManyToManyField(Attente)
    referent = models.ForeignKey('self', blank=True, on_delete=models.PROTECT, null=True, limit_choices_to= models.Q( groups__name = 'Référent'))
    pass
    def __str__(self):
        return self.first_name+" "+self.last_name
    @property
    def is_staff(self):
        return self.groups.filter(name__in=["Référent", "Administrateur"]).exists()

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

    def complet(self):
        return self.nb_inscrits()==self.nb_max_inscrit
    def places_dispo(self):
        return self.nb_max_inscrit-self.nb_inscrits()

    def credits(self):
        return math.ceil((self.date_fin-self.date_debut).total_seconds()/3600)
    def heures(self):
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
    motif = models.TextField(null=True, blank=True)
    def __str__(self):
        return "Réunion entre "+str(self.referent)+" et "+str(self.membre)

class Inscription(models.Model):
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    participation_valide = models.BooleanField(null=True)
    staff = models.BooleanField(null=True)
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
        if self.message:
            return Message.objects.filter(conversation=self.conversation, id__gt=self.message.id).exclude(sender=self.membre).count()
        else:
            return 0

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
        if self.message:
            return MessageGroup.objects.filter(conversation=self.conversation, id__gt=self.message.id).exclude(sender=self.membre).count()
        else:
            return 0

