from django.shortcuts import render
from .models import Produit, Site, Categorie, Utilisateur
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


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

        categorie = Categorie.objects.get(id=categorie_id)
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        site = Site.objects.get(id=site_id)

        produit = Produit(
            code_interne=code_interne,
            marque=marque,
            date_inventaire=date_inventaire,
            categorie=categorie,
            utilisateur=utilisateur,
            site=site
        )

        try:
            produit.save()
            success_message = "Produit ajouté avec succès !"
        except IntegrityError:
            error_message = "Ce code interne existe déjà. Veuillez en choisir un autre."

    sites = Site.objects.all()
    categories = Categorie.objects.all()
    utilisateurs = Utilisateur.objects.all()

    return render(request, 'produit.html', {
        'sites': sites,
        'categories': categories,
        'utilisateurs': utilisateurs,
        'success_message': success_message,
        'error_message': error_message,
    })

from django.http import JsonResponse
from .models import Utilisateur

def get_utilisateurs_par_site(request):
    site_id = request.GET.get('site_id')
    utilisateurs = Utilisateur.objects.filter(site_id=site_id).values('id', 'nom_util')
    return JsonResponse(list(utilisateurs), safe=False)


@login_required(login_url='/login/')
def list_products(request):
    categories = Categorie.objects.all()
    sites = Site.objects.all()
    utilisateurs = Utilisateur.objects.all()

    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')
    search_code = request.GET.get('search_code')

    produits = Produit.objects.all()

    # Apply filtering based on the selected filter type and value
    if filter_type and filter_value:
        if filter_type == 'category':
            produits = produits.filter(categorie_id=filter_value)
        elif filter_type == 'site':
            produits = produits.filter(site_id=filter_value)
        elif filter_type == 'utilisateur':
            produits = produits.filter(utilisateur_id=filter_value)

    # Apply search by internal code
    if search_code:
        produits = produits.filter(code_interne__icontains=search_code)

    return render(request, 'liste_prod.html', {
        'produits': produits,
        'categories': categories,
        'sites': sites,
        'utilisateurs': utilisateurs,
        'selected_filter_type': filter_type,
        'selected_filter_value': filter_value,
        'search_code': search_code,  # Pass the search code to the template
    })

from django.http import JsonResponse
@login_required(login_url='/login/')
def get_filter_values(request):
    filter_type = request.GET.get('filter_type')

    if filter_type == 'category':
        data = list(Categorie.objects.values('id', 'nom_cat'))
    elif filter_type == 'site':
        data = list(Site.objects.values('id', 'nom'))
    elif filter_type == 'utilisateur':
        data = list(Utilisateur.objects.values('id', 'nom_util'))
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
@login_required(login_url='/login/')
def liste_produits_pdf(request):
    filter_type = request.GET.get('filter_type', '')
    filter_value = request.GET.get('filter_value', '')

    # Filtrer les produits en fonction des paramètres de filtrage
    produits = Produit.objects.all()

    if filter_type == 'category' and filter_value:
        produits = produits.filter(categorie_id=filter_value)
    elif filter_type == 'site' and filter_value:
        produits = produits.filter(site_id=filter_value)
    elif filter_type == 'utilisateur' and filter_value:
        produits = produits.filter(utilisateur_id=filter_value)

    template_path = 'export_pdf_template.html'
    context = {'produits': produits}

    # Générer le PDF
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



