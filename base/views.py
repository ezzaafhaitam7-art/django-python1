from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from base.models import Bien
from biens.models import Locataire, Contrat, Paiement  # Importation de tes modèles de gestion
from django.contrib import messages

def est_admin(user):
    return user.is_authenticated and user.is_staff

# --- VUES PUBLIQUES (Accessibles à tous) ---

def home(request):
    return render(request, 'base/home.html')



