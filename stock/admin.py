from django.contrib import admin
from .models import Site, Categorie, Utilisateur, Produit

class SiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'adresse1', 'ville', 'created_at', 'updated_at')
    search_fields = ('nom', 'region', 'ville')
    list_filter = ('region', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom_cat', 'created_at', 'updated_at')
    search_fields = ('nom_cat',)
    readonly_fields = ('created_at', 'updated_at')

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom_util', 'site', 'created_at', 'updated_at')
    search_fields = ('nom_util', 'service')
    list_filter = ( 'site', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('code_interne', 'marque', 'date_inventaire', 'categorie', 'utilisateur', 'site', 'created_at', 'updated_at')
    search_fields = ('code_interne', 'marque', 'categorie__nom_cat', 'utilisateur__nom_util')
    list_filter = ('date_inventaire', 'categorie', 'utilisateur', 'site', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Site, SiteAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Produit, ProduitAdmin)
