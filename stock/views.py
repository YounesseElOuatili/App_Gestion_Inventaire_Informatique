from django.shortcuts import render
from .models import Produit, Site, Categorie, Utilisateur
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


@login_required(login_url='/login/')
def add_product(request):
    error_message = None
    success_message = None

    if request.method == "POST":
        code_interne = request.POST.get('code_interne')
        marque = request.POST.get('marque')
        date_inventaire = request.POST.get('date_inventaire')
        categorie_id = request.POST.get('categorie')
        utilisateur_id = request.POST.get('utilisateur')
        site_id = request.POST.get('site')
        valeur_achat = request.POST.get('valeur_achat')
        date_achat = request.POST.get('date_achat')
        etat = request.POST.get('etat')

        # Vérifiez que tous les champs sont remplis
        if not all([code_interne, marque, date_inventaire, categorie_id, utilisateur_id, site_id, valeur_achat, date_achat, etat]):
            error_message = "Tous les champs doivent être remplis."
        else:
            try:
                categorie = Categorie.objects.get(id=categorie_id)
                utilisateur = Utilisateur.objects.get(id=utilisateur_id)
                site = Site.objects.get(id=site_id)

                produit = Produit(
                    code_interne=code_interne,
                    marque=marque,
                    date_inventaire=date_inventaire,
                    categorie=categorie,
                    utilisateur=utilisateur,
                    site=site,
                    valeur_achat=valeur_achat,
                    date_achat=date_achat,
                    etat=etat
                )

                produit.save()
                success_message = "Produit ajouté avec succès !"
            except IntegrityError:
                error_message = "Ce code interne existe déjà. Veuillez en choisir un autre."
            except ValidationError as ve:
                error_message = f"Erreur de validation: {ve}"
            except Exception as e:
                error_message = f"Une erreur est survenue: {e}"

    sites = Site.objects.all()
    categories = Categorie.objects.all()
    utilisateurs = Utilisateur.objects.all()
    etat_choices = Produit.ETAT_CHOICES

    return render(request, 'produit.html', {
        'sites': sites,
        'categories': categories,
        'utilisateurs': utilisateurs,
        'etat_choices': etat_choices,
        'success_message': success_message,
        'error_message': error_message,
    })


from django.http import JsonResponse
from .models import Utilisateur
from django.db.models import F

def get_utilisateurs_par_site(request):
    site_id = request.GET.get('site_id')
    utilisateurs = Utilisateur.objects.filter(site_id=site_id).values('id', 'nom_util')
    return JsonResponse(list(utilisateurs), safe=False)


@login_required(login_url='/login/')
def list_products(request):
    categories = Categorie.objects.all()
    sites = Site.objects.all()
    utilisateurs = Utilisateur.objects.all()
    
    filter_site = request.GET.get('filter_site')
    filter_category = request.GET.get('filter_category')
    filter_utilisateur = request.GET.get('filter_utilisateur')
    search_code = request.GET.get('search_code')
    sort_by = request.GET.get('sort_by', 'utilisateur')  # Default sorting by 'code_interne'

    produits = Produit.objects.all()

    # Apply filtering based on the selected filter site
    if filter_site:
        produits = produits.filter(site_id=filter_site)
        if filter_category:
            produits = produits.filter(categorie_id=filter_category)
        if filter_utilisateur:
            produits = produits.filter(utilisateur_id=filter_utilisateur)

    # Apply search by internal code
    if search_code:
        produits = produits.filter(code_interne__icontains=search_code)

    # Apply sorting
    valid_sort_fields = ['code_interne', 'marque', 'date_inventaire', 'categorie', 'site', 'utilisateur', 'valeur_achat', 'date_achat', 'etat']
    if sort_by in valid_sort_fields:
        produits = produits.order_by(F(sort_by))

    return render(request, 'liste_prod.html', {
        'produits': produits,
        'categories': categories,
        'sites': sites,
        'utilisateurs': utilisateurs,
        'selected_filter_site': filter_site,
        'selected_filter_category': filter_category,
        'selected_filter_utilisateur': filter_utilisateur,
        'search_code': search_code,
        'selected_sort_by': sort_by,
    })


from django.http import JsonResponse
@login_required(login_url='/login/')
def get_filter_values(request):
    filter_type = request.GET.get('filter_type')
    site_id = request.GET.get('site_id')

    if filter_type == 'category' and site_id:
        data = list(Categorie.objects.filter(produit__site_id=site_id).distinct().values('id', 'nom_cat'))
    elif filter_type == 'site':
        data = list(Site.objects.values('id', 'nom'))
    elif filter_type == 'utilisateur' and site_id:
        data = list(Utilisateur.objects.filter(site_id=site_id).values('id', 'nom_util'))
    else:
        data = []

    return JsonResponse(data, safe=False)



# stock/views.py

from django.shortcuts import render, redirect
from .models import Utilisateur, Site  # Adjust according to your model names

@login_required(login_url='/login/')
def add_utilisateur(request):
    if request.method == 'POST':
        nom_util = request.POST.get('nom_util')
        site_id = request.POST.get('site')
        site = Site.objects.get(id=site_id)  # Ensure you have Site model imported
        
        if nom_util and site:
            Utilisateur.objects.create(
                nom_util=nom_util,

                site=site
            )
            success_message = "Utilisateur ajouté avec succès !"
            return render(request, 'utilisateur.html', {'success_message': success_message, 'sites': Site.objects.all()})
    
    return render(request, 'utilisateur.html', {'sites': Site.objects.all()})

@login_required(login_url='/login/')
def liste_utilisateurs(request):
    # Filtrage des utilisateurs par site
    site_id = request.GET.get('site')
    if site_id:
        utilisateurs = Utilisateur.objects.filter(site_id=site_id)
    else:
        utilisateurs = Utilisateur.objects.all()

    sites = Site.objects.all()
    selected_site = site_id if site_id else ''

    return render(request, 'liste_util.html', {
        'utilisateurs': utilisateurs,
        'sites': sites,
        'selected_site': selected_site,
    })



from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from .models import Produit, Categorie, Site, Utilisateur
from django.db.models import F

@login_required(login_url='/login/')
def liste_produits_pdf(request):
    # Récupérer les mêmes paramètres de filtrage que ceux utilisés dans list_products
    filter_site = request.GET.get('filter_site')
    filter_category = request.GET.get('filter_category')
    filter_utilisateur = request.GET.get('filter_utilisateur')
    search_code = request.GET.get('search_code')
    sort_by = request.GET.get('sort_by', 'code_interne')  # Par défaut, trier par 'code_interne'

    produits = Produit.objects.all()

    # Appliquer les filtres en fonction des paramètres
    if filter_site:
        produits = produits.filter(site_id=filter_site)
        if filter_category:
            produits = produits.filter(categorie_id=filter_category)
        if filter_utilisateur:
            produits = produits.filter(utilisateur_id=filter_utilisateur)

    # Appliquer la recherche par code interne
    if search_code:
        produits = produits.filter(code_interne__icontains=search_code)

    # Appliquer le tri
    valid_sort_fields = ['code_interne', 'marque', 'date_inventaire', 'categorie', 'site', 'utilisateur', 'valeur_achat', 'date_achat', 'etat']
    if sort_by in valid_sort_fields:
        produits = produits.order_by(F(sort_by))

    # Passer les produits filtrés au template
    context = {'produits': produits}

    # Générer le PDF
    template_path = 'export_pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_produits.pdf"'

    # Utiliser xhtml2pdf pour générer le PDF
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response



# stock/views.py
# views.py



