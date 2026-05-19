from django.db import models
from django.contrib.auth.models import User
from base.models import Bien
from datetime import date, timedelta

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=100)
    cin = models.CharField(max_length=20, unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    profession = models.CharField(max_length=100)
    date_naissance = models.DateField()

    def __str__(self):
        return self.nom_complet

class Locataire(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200, blank=True, null=True) 
    email = models.EmailField(max_length=200)
    telephone = models.CharField(max_length=20) 

    def __str__(self):
        return f"{self.nom}"

class Contrat(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        
        return f"{self.locataire.nom} - {self.bien.Titre}"

class Paiement(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE)
    montant = models.FloatField()
    date_paiement = models.DateField()
    statut = models.CharField(max_length=50)   

    def __str__(self):
        return f"{self.contrat} - {self.montant} DH"

class Demande(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Acceptée', 'Acceptée'),
        ('Refusée', 'Refusée'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En attente')
    message = models.TextField(blank=True, null=True, verbose_name="Message du client")

    def save(self, *args, **kwargs):
        statut_avant = None
        if self.pk:
            ancien = Demande.objects.filter(pk=self.pk).values('statut').first()
            if ancien:
                statut_avant = ancien['statut']

        super().save(*args, **kwargs)

        if self.statut == 'Acceptée' and statut_avant != 'Acceptée':
            self._creer_locataire_contrat_paiement()

    def _creer_locataire_contrat_paiement(self):
        client = self.client
        email_locataire = client.user.email or f"{client.user.username}@example.com"

        locataire, created = Locataire.objects.get_or_create(
            email=email_locataire,
            defaults={
                'nom': client.nom_complet,
                'prenom': client.cin,
                'telephone': client.telephone
            }
        )

        if not Contrat.objects.filter(bien=self.bien, locataire=locataire).exists():
            contrat = Contrat.objects.create(
                bien=self.bien,
                locataire=locataire,
                date_debut=date.today(),
                date_fin=date.today() + timedelta(days=365)
            )
            Paiement.objects.create(
                contrat=contrat,
                montant=float(str(self.bien.Prix).replace(',', '.')),
                date_paiement=date.today(),
                statut='Payé'
            )

        self.bien.Statut = 'Loué'
        self.bien.save()

    def __str__(self):
        return f"Demande de {self.client.nom_complet} - {self.bien.Titre} ({self.statut})"
