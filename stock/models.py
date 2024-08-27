from django.db import models
from base.models import  Regions
from datetime import date
# Create your models here.

class Site(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom = models.CharField(max_length = 30, verbose_name = "Nom")
    adresse1 = models.CharField(max_length =30, verbose_name = "Adresse",null = True, blank = True)
    ville = models.CharField(max_length =15, verbose_name = "Ville",null = True, blank = True)
    region = models.CharField(max_length = 6, verbose_name = "Région",choices=Regions.choices)

    def __str__(self):
        return self.nom
class Categorie(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom_cat = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nom_cat

class Utilisateur(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom_util = models.CharField(max_length=100)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nom_util

class Produit(models.Model):
    ETAT_CHOICES = [
        ('en_service', 'En service'),
        ('en_stock', 'En stock'),
        ('en_cours_de_maintenance', 'En cours de maintenance'),
        ('hors_service', 'Hors service'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code_interne = models.CharField(max_length=100, unique=True)
    marque = models.CharField(max_length=100)
    date_inventaire = models.DateField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    valeur_achat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    date_achat = models.DateField(null=True, blank=True, default=date.today)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES, default='en_service')

    def __str__(self):
        return self.code_interne


