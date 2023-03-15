from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.timezone import now
import math
# Create your models here.

"""Définition des différentes classes/tables du projet"""

class Competence(models.Model):
    """ Compétences d'un membre
    
    :param nom: Nom de la compétence
    """
    nom = models.CharField(max_length=200, null=False, primary_key=True)
    def __str__(self):
        """Affichage par défaut de la compétence"""
        return self.nom

class Attente(models.Model):
    """ Attentes d'un membre
    
    :param nom: Nom de l'attente
    """
    nom = models.CharField(max_length=200, null=False, primary_key=True)
    def __str__(self):
        """Affichage par défaut de l'attente"""
        return self.nom
        
class Membre(AbstractUser):
    """ Compte d'un utilisateur
    
    :param int id: ID de l'utilisateur.
    :param str email: Email de l'utilisateur.
    :param str password: Mot de passe haché de l'utilisateur.
    :param str username: Nom d'utilisateur.
    :param str first_name: Prénom de l'utilisateur.
    :param str last_name: Nom de famille de l'utilisateur.
    :param str photo: URL de la photo de profil.
    :param str cat_sociopro: Catégorie socioprofessionnelle.
    :param str phone: Numéro de téléphone.
    :param float nb_heures: Nombre d'heures effectuées.
    :param int credits: Nombre de crédits possédés.
    :param Membre referent: ID du référent si l'utilisateur est adhérent.
    :param date last_login: Date de dernière connexion.
    :param date date_join: Date de création du compte.
    :param bool is_superuser: Est super-utilisateur ?
    :param bool is_staff: Peut accéder au panneau d'administration ?
    :param bool is_active: Le compte est activé ?
    """
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
    nb_heures = models.FloatField(default=0, null=False)
    credits = models.IntegerField(default=0, null=False)
    competences = models.ManyToManyField(Competence)
    attentes = models.ManyToManyField(Attente)
    referent = models.ForeignKey('self', blank=True, on_delete=models.PROTECT, null=True, limit_choices_to= models.Q( groups__name__in = ['Référent', 'Administrateur']))
    pass
    def __str__(self):
        """Affichage par défaut du membre"""
        return self.first_name+" "+self.last_name

class Vacation(models.Model):
    """ Définition d'une vacation

    :param date date_debut: Date et heure de début
    :param date date_fin: Date et heure de fin
    :param str nom: Nom de la vacation
    :param str description: Description de la vacation
    :param int nb_max_inscrit: Nombre maximum d'inscription
    :param Competence categorie: Compétences liées à la vacation

    """
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True)
    nb_max_inscrit = models.IntegerField(default=0, null=True)
    categorie = models.ManyToManyField(Competence)
    
    def __str__(self):
        """Affichage par défaut d'une vacation"""
        return self.nom+" ("+self.date_debut.strftime("%d/%m/%Y")+")"

    def nb_inscrits(self):
        """Renvoi le nombre de personnes inscrites à la vacation
        
        :rtype: int
        """
        return Inscription.objects.filter(vacation=self.id).count()

    def complet(self):
        """Indique si la vacation est complète
        
        :rtype: bool
        """
        return self.nb_inscrits()==self.nb_max_inscrit
    def places_dispo(self):
        """Renvoi le nombre de places disponibles
        
        :rtype: int
        """
        return self.nb_max_inscrit-self.nb_inscrits()

    def credits(self):
        """Renvoi le nombre de crédits que va rapporter la vacation
        
        :rtype: int
        """
        return math.ceil((self.date_fin-self.date_debut).total_seconds()/3600)
    def heures(self):
        """Renvoi la durée de la vacation
        
        :rtype: int
        """
        return math.ceil((self.date_fin-self.date_debut).total_seconds()/3600)
    def inscrits(self):
        """Renvoi la liste des inscrits à la vacation
        
        :rtype: list
        """
        return Inscription.objects.filter(vacation=self.id).values_list('membre')

class Contrepartie(models.Model):
    """ Définition d'une contrepartie

    :param str nom: Nom de la contrepartie
    :param str details: Description de la contrepartie
    :param int credits_requis: Nombre de crédits requis pour récupérer la contrepartie
    :param int quantite_dispo: Quantité disponible de la contrepartie
    :param Attente attente: Attentes liées à la contrepartie

    """
    nom = models.CharField(max_length=100)
    details = models.TextField(default="")
    credits_requis = models.IntegerField(default=0, null=True)
    quantite_dispo = models.IntegerField(default=0, null=True)
    attente = models.ManyToManyField(Attente)
    def __str__(self):
        """Affichage par défaut d'une contrepartie"""
        return self.nom+" ("+str(self.quantite_dispo)+")"

class Reunion(models.Model):
    """ Définition d'une réunion

    :param date date: Date et heure de la réunion
    :param Membre referent: Référent lié à la réunion
    :param Membre membre: Adhérent lié à la réunion
    :param str contenu: Contenu de la réunion
    :param str motif: Motif de la réunion

    """
    date = models.DateTimeField()
    referent = models.ForeignKey(Membre, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="membres")
    contenu = models.TextField(null=True, blank=True)
    motif = models.TextField(null=True, blank=True)
    def __str__(self):
        """Affichage par défaut d'une réunion"""
        return "Réunion entre "+str(self.referent)+" et "+str(self.membre)

class Inscription(models.Model):
    """ Définition d'une incription à une vacation

    :param Vacation vacation: Vacation liée à l'inscription
    :param Membre membre: Membre lié à l'inscription
    :param bool participation_valide: Indique si la participation à été validée ou non
    :param bool staff: Indique si l'inscription est de type staff ou non

    """
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    participation_valide = models.BooleanField(null=True)
    staff = models.BooleanField(null=True)
    def __str__(self):
        """Affichage par défaut d'une inscription"""
        return str(self.membre)+" est inscrit à "+str(self.vacation)

class Choix(models.Model):
    """ Définition d'un choix de contrepartie

    :param Contrepartie contrepartie: Contrepartie liée au choix
    :param Membre membre: Membre lié au choix
    :param bool recupere: Indique si la contrepartie à été récupérée
    :param date date: Date du choix de la contrepartie

    """
    contrepartie = models.ForeignKey(Contrepartie, on_delete=models.PROTECT)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    recupere = models.BooleanField(default=False, verbose_name="récupéré ?")
    date = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        """Affichage par défaut d'un choix"""
        return str(self.membre)+" a choisi la contrepartie : "+self.contrepartie.nom
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['contrepartie', 'membre', 'date'], name='unique_contrepartie_mail_combination'
            )
        ]
        verbose_name_plural = "Choix"
class Conversation(models.Model):
    """ Définition d'une conversation 1o1

    :param Membre pers1: Membre de la conversation
    :param Membre pers2: Membre de la conversation

    """
    pers1=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name='pers1')
    pers2=models.ForeignKey(Membre, on_delete=models.CASCADE)
    def __str__(self):
        """Affichage par défaut d'une conversation"""
        return str(self.pers1)+" "+str(self.pers2)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender=models.ForeignKey(Membre, null=True, on_delete=models.SET_NULL)
    message = models.TextField(null=True)
    date = models.DateTimeField()
    def __str__(self):
        """Affichage par défaut d'un message"""
        return str(self.conversation)+" "+str(self.date)

class MessageGroup(models.Model):
    conversation = models.ForeignKey(Vacation, on_delete=models.CASCADE)
    sender=models.ForeignKey(Membre, null=True, on_delete=models.SET_NULL)
    message = models.TextField(null=True)
    date = models.DateTimeField()
    def __str__(self):
        """Affichage par défaut d'un message de groupe"""
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
            return Message.objects.filter(conversation=self.conversation).exclude(sender=self.membre).count()

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

