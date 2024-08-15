# stock/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('list_products/', views.list_products, name='list_products'), 
    path('get_filter_values/', views.get_filter_values, name='get_filter_values'),
    path('add_utilisateur/', views.add_utilisateur, name='add_utilisateur'),
    path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('liste-produits-pdf/', views.liste_produits_pdf, name='liste_produits_pdf'),
    
]
