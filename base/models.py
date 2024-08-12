from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from crum import get_current_user
from django.utils.formats import date_format
from django.apps import apps
from django.db.models import Q, Count
from tree_queries.models import TreeNode
from tree_queries.query import TreeQuerySet, TreeManager
from django.utils.html import format_html, mark_safe
from django.utils.functional import lazy



# On commence par définir les object managers par défaut pour les querysets

#Pour le modèle Site uniquement
class SiteObjectsManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if user and user.is_anonymous and hasattr(user, "device") and user.device:
            return super().get_queryset().filter(actif = True , pk__in = [user.device.site.pk,])
        if not user or user.is_anonymous:
            return super().get_queryset().none()
        if user.is_superuser:
            return super().get_queryset().filter(actif = True)
        return super().get_queryset().filter(actif = True , user__in = [user.pk,])

#Pour les objets de configuration qui possèdent un site
class ConfigObjectsManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if user and user.is_anonymous  and hasattr(user, "device") and user.device:
            return super().get_queryset().filter(actif = True , site__in = [user.device.site.pk,])
        if not user or user.is_anonymous:
            return super().get_queryset().none()
        if user.is_superuser:
            return super().get_queryset().filter(actif = True)
        return super().get_queryset().filter(actif = True , site__in = user.sites.all())

#Pour les objets de configuration qui ne possèdent pas de site (produits, catégories,...)
class SitelessConfigObjectsManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if user and user.is_anonymous  and hasattr(user, "device") and user.device:
            return super().get_queryset().all()
        if not user or user.is_anonymous:
            return super().get_queryset().none()
        return super().get_queryset().filter(actif = True)

#Pour les objets de configuration qui possèdent un site mais pas de champ actif



#Tous les objets
class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class PerimeterQuerySet(TreeQuerySet):
    def active(self):
        user = get_current_user()
        if user and user.is_anonymous  and hasattr(user, "device") and user.device:
            return self.filter(actif = True , site__in = [user.device.site.pk,])
        if not user or user.is_anonymous:
            return self.none()
        if user.is_superuser:
            return self.filter(actif = True)
        return self.filter(actif = True , site__in = user.sites.all())

PerimeterObjectsManager = TreeQuerySet.as_manager(with_tree_fields=True)


# #Pour les objets de périmètre qui possèdent un site
class PerimeterObjectsManager(TreeManager):
    @classmethod
    def cast(cls, some_a: TreeManager):
        """Cast an A into a MyA."""
        assert isinstance(some_a, TreeManager)
        some_a._class_ = cls  # now mymethod() is available
        assert isinstance(some_a, PerimeterObjectsManager)
        some_a._with_tree_fields = True
        return some_a
    def get_queryset(self):
        user = get_current_user()
        if user and user.is_anonymous  and hasattr(user, "device") and user.device:
            return super().get_queryset().with_tree_fields().filter(actif = True , site__in = [user.device.site.pk,])
        if not user or user.is_anonymous:
            return super().get_queryset().none()
        if user.is_superuser:
            return super().get_queryset().filter(actif = True)
        return super().get_queryset().with_tree_fields().filter(actif = True , site__in = user.sites.all())



def get_readable_distance(meter_distance):
    if meter_distance == 0:
        return 0
    elif meter_distance < 1000:
        return str(int(meter_distance)) + " m"
    return str(round(meter_distance /1000 , 1)) + " km"

def get_readable_duration(seconds_duration):
    if seconds_duration == 0:
        return 0 + " min"
    elif seconds_duration < 60:
        return str(int(seconds_duration)) + " s"
    elif seconds_duration < 3600:
        return str(int(seconds_duration/60)) + " min"
    return str(int(seconds_duration/3600)) + " h " + str(int((seconds_duration%3600)/60)) + " min"

def get_excel_duration(seconds_duration):
    if seconds_duration == 0:
        return "00:00:00"
    seconds = seconds_duration % 60
    remaining_seconds = seconds_duration - seconds
    minutes = (remaining_seconds % 3600) / 60
    remaining_seconds = remaining_seconds - (minutes * 60)
    hours = remaining_seconds / 3600
    return "{0:02d}:{1:02d}:{2:02d}".format(int(hours), int(minutes), int(seconds))



# Inutile mais nécessaire pour la migration. Bug de Django
def order_attachments_upload_to(instance, filename):
    return



class Societe(models.Model):
    FORMES = (
        ('sarl', 'SARL'),
        ('sarlau', 'SARL AU'),
        ('sa', 'SA'),
    )
    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Sociétés"
        default_permissions = ['add', 'change', 'view']
        db_table = "base_company"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Société"
    nom = models.CharField(max_length = 30, verbose_name = "Raison sociale")
    phone = models.CharField(max_length = 16, verbose_name = "Téléphone",null = True, blank = True)
    adresse1 = models.CharField(max_length =30, verbose_name = "Adresse",null = True, blank = True)
    adresse2 = models.CharField(max_length =30, verbose_name = "Suite",null = True, blank = True)
    ville = models.CharField(max_length =15, verbose_name = "Ville")
    patente = models.CharField(max_length =15, verbose_name = "Patente",null = True, blank = True)
    rc = models.CharField(max_length =15, verbose_name = "Registre de commerce",null = True, blank = True)
    cnss = models.CharField(max_length =15, verbose_name = "Num CNSS",null = True, blank = True)
    idf = models.CharField(max_length =15, verbose_name = "Identifiant fiscal",null = True, blank = True)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    ice = models.CharField(max_length =15, verbose_name = "ICE",null = True, blank = True)
    logo = models.ImageField(upload_to='logo',blank=True,null=True, verbose_name = "Logo")
    forme = models.CharField(max_length = 10, verbose_name = "Forme juridique",choices=FORMES,null = True, blank = True)
    def _str_(self):
        if self.forme:
            return "{0} {1}".format(self.nom, self.get_forme_display())
        else:
            return self.nom
    def clean(self):
        if not self.actif and not self.pk : 
            raise ValidationError({'actif': ("L'objet doit être actif lors de sa création.")})

def replace_sequence_placeholders( s , site ):
    if not s:
        return ""

    aujourdhui  = datetime.date.today()
    s = s.replace("$(YYYY)", aujourdhui.strftime('%Y'))
    s = s.replace("$(YY)", aujourdhui.strftime('%y'))
    s = s.replace("$(MM)", aujourdhui.strftime('%m'))
    s = s.replace("$(DD)", aujourdhui.strftime("%d"))
    s = s.replace("$(SITE)", site.ref)
    return s

def get_default_max_delivery_number():
    return settings.DISPATCH_MAX_DELIVERY_NUMBER if hasattr(settings, "DISPATCH_MAX_DELIVERY_NUMBER") else 1000

def get_default_max_duration():
    return settings.DEFAULT_MAX_TIME_FOR_DELIVERY
def get_default_heure_depart():
    return settings.DEFAULT_HEURE_DEPART_VEHICULES

def get_availability_methods_choices():
    base_methods = (
        ('none', 'Aucune'),
        ("manual", "Manuelle - Saisie manuelle des disponibilités"),        
    )
    if "stock" in settings.INSTALLED_APPS:
        base_methods += (
            ("stockouts", "Ruptures de stock - Saisie des ruptures de stock"),
            # ("stock", "Stock - Quantités en stock"),
        )
    return base_methods

def get_default_odometer_check():
    return settings.VEHICLE_ENABLE_ODOMETER_CHECKS if hasattr(settings, "VEHICLE_ENABLE_ODOMETER_CHECKS") else False

def get_default_lifo_loading():
    return settings.ENABLE_LIFO_LOADING if hasattr(settings, "ENABLE_LIFO_LOADING") else False



class Regions(models.TextChoices):
    MA01 = "MA01", "Tanger-Tétouan-Al Hoceïma"
    MA02 = "MA02", "L'Oriental"
    MA03 = "MA03", "Fès-Meknès"
    MA04 = "MA04", "Rabat-Salé-Kénitra"
    MA05 = "MA05", "Béni Mellal-Khénifra"
    MA06 = "MA06", "Casablanca-Settat"
    MA07 = "MA07", "Marrakech-Safi"
    MA08 = "MA08", "Drâa-Tafilalet"
    MA09 = "MA09", "Souss-Massa"
    MA10 = "MA10", "Guelmim-Oued Noun"
    MA11 = "MA11", "Laâyoune-Sakia El Hamra"
    MA12 = "MA12", "Dakhla-Oued Ed-Dahab"
    ATRE = "ATRE", "Autre / Etranger"


class Site(models.Model):
    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Sites"
        permissions = (
            ('can_access_hht_parameters', 'Gestion des HHT'),
            ('is_admin_for_hht', 'Mode administrateur pour'),
        )
        default_permissions = ['add', 'change', 'view']
        db_table = "base_site"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Site"
    nom = models.CharField(max_length = 30, verbose_name = "Nom")
    adresse1 = models.CharField(max_length =30, verbose_name = "Adresse",null = True, blank = True)
    adresse2 = models.CharField(max_length =30, verbose_name = "Suite",null = True, blank = True)
    ville = models.CharField(max_length =15, verbose_name = "Ville",null = True, blank = True)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    history = HistoricalRecords(table_name="base_site_history")
    region = models.CharField(max_length = 6, verbose_name = "Région",choices=Regions.choices)
    objects = SiteObjectsManager()
    allobjects = AllObjectsManager()


    def __init__(self, *args, **kwargs):
        super(Site, self).__init__(*args, **kwargs)
        if any(field.name == 'availability_check_method' for field in self._meta.get_fields()):
            self._meta.get_field('availability_check_method').choices = lazy(get_availability_methods_choices, list)()

    def _str_(self):
        return self.nom

    def invoice_footer(self, *args, **kwargs):
        first_line = self.societe
        if self.societe_obj.phone:
            first_line += " - Tél: " + self.societe_obj.phone
        elif self.phone:
            first_line += " - Tél: " + self.phone

        if self.ice:
            first_line += " - ICE: " + self.ice
        second_line = ""
        if self.idf:
            second_line += "Identifiant Fiscal: " + self.idf
        if self.patente:
            if second_line != "":
                second_line += " - "
            second_line += "Patente: " + self.societe_obj.patente
        if self.rc:
            if second_line != "":
                second_line += " - "
            second_line += "RC: " + self.rc
        if self.cnss:
            if second_line != "":
                second_line += " - "
            second_line += "CNSS: " + self.cnss

        if second_line == "":
            return ("",first_line)
        return (first_line, second_line)
      

   
    @property
    def ice(self):
        return self.societe_obj.ice
    @property
    def rc(self):
        return self.societe_obj.rc
    @property
    def cnss(self):
        return self.societe_obj.cnss
    @property
    def societe(self):
        return str(self.societe_obj)
    @property
    def idf(self):
        return self.societe_obj.idf
    @property
    def logo(self):
        return self.societe_obj.logo
    def clean(self):
        if not self.actif and not self.pk : 
            raise ValidationError({'actif': ("L'objet doit être actif lors de sa création.")})
        if self.pk and not self.actif:
            orders = self.order_set.exclude(etat__in=('cancel','done'))
            if self.order_set.exclude(etat__in=('cancel','done')):
                raise ValidationError({'actif': ('Ce site ne peut pas être désactivé. Des commandes ne sont pas encore terminées.')})
            if self.delivery_set.exclude(etat__in=('cancel','done')):
                raise ValidationError({'actif': ('Ce site ne peut pas être désactivé. Des livraisons ne sont pas encore terminées.')})
            if self.tournee_set.exclude(etat__in=('cancel','done')):
                raise ValidationError({'actif': ('Ce site ne peut pas être désactivé. Des tournées ne sont pas encore terminées.')})
            if self.vehicules.exclude(actif = False):
                raise ValidationError({'actif': ('Ce site ne peut pas être désactivé. Des véhicules lui sont toujours associés.')})
            if self.client_set.exclude(actif = False):
                raise ValidationError({'actif': ('Ce site ne peut pas être désactivé. Des clients lui sont toujours associés.')})
           

    def get_so_serial(self):
        if not self.sequences : 
            site_sequences = SiteSequences(site=self)
            site_sequences.save()

        prefix = replace_sequence_placeholders(self.sequences.so_prefix, self)
        suffix = replace_sequence_placeholders(self.sequences.so_suffix, self)

        external_id = prefix + str(self.sequences.so_last_sequence + 1).zfill(self.sequences.so_nb_digits) + suffix
        self.sequences.so_last_sequence = self.sequences.so_last_sequence+1
        self.sequences.save()

        return external_id

    @property
    def is_lifo_loading_enabled(self):
        if not hasattr(settings, "ENABLE_LIFO_LOADING") or not settings.ENABLE_LIFO_LOADING:
            return False
        return self.enbale_lifo_loading

phone_regex = RegexValidator(
    regex=r'^0(|.| |-)(5|6|7|8)((|.| |-)[0-9]){8}$',
    message='Le numéro de téléphone est incorrect.'
)

from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    class Meta:
        default_permissions = ['add', 'change', 'view']
        verbose_name = ('Utilisateur')
        verbose_name_plural = ('Utilisateurs')
        db_table = "base_user"
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change 'custom_user_set' to any unique name you prefer
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change 'custom_user_set' to any unique name you prefer
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(validators=[phone_regex], max_length=20, null=True, blank=True, verbose_name = "Numéro de téléphone")
    sites = models.ManyToManyField('Site', blank = True, verbose_name = "Sites", limit_choices_to={'actif': True})
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name = "Email")
    login_from_outside = models.BooleanField(default=False, verbose_name = "Peut se connecter de l'extérieur?",
                                help_text="Si coché, l'utilisateur pourra se connecter depuis l'extérieur de l'entreprise.")
    history = HistoricalRecords(table_name="base_user_history")
    def _str_(self):
        return self.get_full_name()

