from django.urls import path
from . import views
from base import views as base_views
urlpatterns = [
    path('logout/', views.deconnexion_manuelle, name='logout'),

    path('', views.liste_biens, name='biens'),
    path('bien/<int:pk>/', views.bien_detail, name='bien_detail'),
    path('', views.liste_biens, name='biens'),
    path('inscription/', views.inscription, name='inscription'),
    path('mes-demandes/', views.mes_demandes, name='mes_demandes'),
    path('locataires/', views.liste_locataires, name='locataires'),
    path('contrats/', views.liste_contrats, name='contrats'),
    path('paiements/', views.liste_paiements, name='paiements'),
    path('louer/<int:bien_id>/', views.louer_bien, name='louer_bien'),
    path('login/', views.login_personnalise, name='mon_login'),
    path('gestion-demandes/', views.gestion_demandes, name='gestion_demandes'),
    path('accepter-demande/<int:pk>/', views.accepter_demande, name='accepter_demande'),
    path('refuser-demande/<int:pk>/', views.refuser_demande, name='refuser_demande'),
]
