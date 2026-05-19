from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout 

from base.models import Bien
from .models import Locataire, Contrat, Paiement, Demande
from .models import Client
from datetime import date, timedelta


def liste_biens(request):
    biens = Bien.objects.all()
    return render(request, 'base/biens.html', {'biens': biens})

def bien_detail(request, pk):
    bien = get_object_or_404(Bien, pk=pk)
    return render(request, 'base/bien_detail.html', {'bien': bien})

def louer_bien(request, bien_id):
    bien = get_object_or_404(Bien, id=bien_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
               
        try:
            profil_client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:

            return render(request, 'base/erreur.html', {
                'message': "Erreur : Votre profil client n'existe pas. Veuillez vous inscrire via le formulaire."
            })


        Demande.objects.create(
            client=profil_client,  
            bien=bien,
            message=message,
            statut='En attente'
        )
        
        return redirect('mes_demandes')

    return render(request, 'base/louer_form.html', {'bien': bien})
# --- SYSTÈME DE CONNEXION ---

def login_personnalise(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('/') 
        else:
            messages.error(request, "Identifiants invalides")
    return render(request, 'base/login.html')
# --- VUES PROTÉGÉES (Redirigent vers ton login personnalisé) ---

@login_required(login_url='/biens/login/')
def liste_locataires(request):
    locataires = Locataire.objects.all()
    return render(request, 'base/locataires.html', {'locataires': locataires})

@login_required(login_url='/biens/login/')
def liste_contrats(request):
    contrats = Contrat.objects.all()
    return render(request, 'base/contrats.html', {'contrats': contrats})

@login_required(login_url='/biens/login/')
def liste_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, 'base/paiements.html', {'paiements': paiements})



def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # On récupère les valeurs via les attributs 'name' du HTML
            Client.objects.create(
                user=user,
                nom_complet=request.POST.get('nom_complet'),
                cin=request.POST.get('cin'),
                telephone=request.POST.get('telephone'),
                adresse=request.POST.get('adresse'),
                profession=request.POST.get('profession'),
                date_naissance=request.POST.get('date_naissance')
            )
            return render(request, 'base/inscription_succes.html')
    else:
        form = UserCreationForm()
    return render(request, 'base/inscription.html', {'form': form})

@login_required(login_url='mon_login')
def mes_demandes(request):
    try:
        profil_client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return render(request, 'base/erreur.html', {
            'message': "Profil client introuvable. Veuillez compléter votre inscription."
        })

    
    demandes = Demande.objects.filter(client=profil_client)

    return render(request, 'base/mes_demandes.html', {'demandes': demandes})

def deconnexion_manuelle(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    return redirect('/')


@login_required(login_url='mon_login')
def gestion_demandes(request):
   
    
    demandes = Demande.objects.all().order_by('-date_demande')
    return render(request, 'base/gestion_demandes.html', {'demandes': demandes})


@login_required(login_url='mon_login')

@login_required(login_url='mon_login')
def accepter_demande(request, pk):
    

    demande = get_object_or_404(Demande, pk=pk)
    client = demande.client
    bien = demande.bien

    try:
        # 1. Créer le Locataire d'abord
        # On utilise l'email pour vérifier s'il existe déjà
        locataire, created = Locataire.objects.get_or_create(
            email=client.user.email,
            defaults={
                'nom': client.nom_complet,
                'prenom': client.cin,
                'telephone': client.telephone
            }
        )

        # 2. Créer le Contrat
        nouveau_contrat = Contrat.objects.create(
            bien=bien,
            locataire=locataire,
            date_debut=date.today(),
            date_fin=date.today() + timedelta(days=365)
        )

        # 3. Créer le Paiement (On convertit le prix en nombre pur)
        # On utilise float() seulement si bien.Prix est une chaîne, sinon direct
        montant_final = float(str(bien.Prix).replace(',', '.')) 
        
        Paiement.objects.create(
            contrat=nouveau_contrat,
            montant=montant_final,
            date_paiement=date.today(),
            statut='Payé'
        )

        demande.statut = 'Acceptée'
        demande.save()
        
        bien.Statut = 'Loué'
        bien.save()

        messages.success(request, f"Succès ! {client.nom_complet} est maintenant locataire et le contrat est généré.")

    except Exception as e:
        messages.error(request, f"Erreur lors de la création : {str(e)}")
        print(f"DEBUG ERREUR: {e}")

    return redirect('gestion_demandes')

@login_required(login_url='mon_login')
def refuser_demande(request, pk):
    # Sécurité : Seul Haitam peut refuser
    if not request.user.is_staff:
        return redirect('/')
        
    demande = get_object_or_404(Demande, pk=pk)
    
    # On change simplement le statut sans créer de locataire ou contrat
    demande.statut = 'Refusée'
    demande.save()
    
    messages.warning(request, f"La demande de {demande.client.nom_complet} a été refusée.")
    return redirect('gestion_demandes')
