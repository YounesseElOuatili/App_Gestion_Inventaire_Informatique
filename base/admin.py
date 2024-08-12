from django.contrib import admin
from .models import (
    Societe,
    Site,
   

    User
)

class SocieteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'forme', 'phone', 'adresse1', 'adresse2', 'ville', 'actif')
    search_fields = ('nom', 'forme', 'phone')
    list_filter = ('forme', 'actif')
    readonly_fields = ('created_at', 'updated_at')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'adresse1', 'adresse2', 'ville', 'actif')
    search_fields = ('nom', 'region')
    list_filter = ( 'region', 'actif')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Site, SiteAdmin)









class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'get_last_password_change')  # Assurez-vous que ces attributs existent
    readonly_fields = ('created_at', 'updated_at', 'get_last_password_change')  # Assurez-vous que ces attributs existent
    
    def get_last_password_change(self, obj):
        """Affiche la dernière modification du mot de passe pour l'utilisateur."""
        if hasattr(obj, 'passwordchange'):
            return obj.get_last_password_change
        return "Non disponible"

    get_last_password_change.short_description = 'Dernière modification du mot de passe'




# Enregistrement des modèles avec l'administration Django
admin.site.register(Societe, SocieteAdmin)



admin.site.register(User, UserAdmin)

