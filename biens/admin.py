from django.contrib import admin
from .models import Locataire, Contrat, Paiement, Demande, Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'cin', 'telephone', 'profession')
    search_fields = ('nom_complet', 'cin')

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('client', 'bien', 'date_demande', 'statut', 'message')
    
    list_editable = ('statut',)
    
    list_filter = ('statut', 'date_demande')
    
    search_fields = ('client__nom_complet', 'client__cin', 'bien__Titre')

@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone')

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('bien', 'locataire', 'date_debut', 'date_fin')

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('contrat', 'montant', 'date_paiement', 'statut')
    list_filter = ('statut',)
