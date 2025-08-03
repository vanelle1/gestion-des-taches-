# © 2025 Tagang Vanelle
# Licensed under the MIT License – See LICENSE file for details


import base64
import datetime
import io
from itertools import product
import os
from django.conf import settings
from django.contrib.auth.models import User
from pyexpat.errors import messages
from turtle import pd
from matplotlib import pyplot as plt
import requests
from django.db.models import F
from django.contrib import messages
from .models import Facture, Fournisseur, Paiement, Product, Promotion, RetourProduit
from .forms import FournisseurForm, PaiementForm, ProductForm, PromotionForm, RetourProduitForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Client, Commande
from .forms import ClientForm, CommandeForm
from .models import DetailCommande
from .forms import DetailCommandeForm
from django.shortcuts import render, redirect
import csv
from django.http import Http404, HttpResponse
from .models import Livraison
from .forms import LivraisonForm
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models import Count
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import user_passes_test

def est_admin(user):
    return user.groups.filter(name='Admin').exists()

@user_passes_test(est_admin)
def vue_admin(request):
    return render(request, 'admin_page.html')
GOOGLE_MAPS_API_KEY = "VOTRE_CLE_API"

def base(request):
    return render(request, 'shop/base.html')

@permission_required('shop.view_product')
def product_list(request):
    products = Product.objects.all()
    
    produits_en_alerte = products.filter(stock__lte=F('seuil_alerte'))

    if produits_en_alerte.exists():
        messages.warning(request, "⚠️ Certains produits ont un stock insuffisant ! Veuillez réapprovisionner.")

    return render(request, 'shop/product_list.html', {'products': products})
@permission_required('shop.view_product')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)## Création de l'objet formulaire avec les données POST
        if form.is_valid():##Vérification de la validité du formulaire
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def home1(request):
    return render(request, 'shop/home1.html')

def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('add_product')  # Redirection vers la page d'accueil après connexion
            else:
                return render(request, 'shop/login.html', {'form': form, 'error': 'Nom d’utilisateur ou mot de passe incorrect'})
    else:
        form = LoginForm()
    
    return render(request, 'shop/login.html', {'form': form})


# # Vue protégée qui nécessite une connexion
@login_required
def ma_vue(request):
   return render(request, 'product_list.html') 


def product_update(request, pk):
     product = get_object_or_404(Product, pk=pk)##Récupération du produit à mettre à jour (get_object_or_404)
     if request.method == 'POST':##Vérification de la méthode de la requête
         form = ProductForm(request.POST, instance=product)##Création du formulaire avec les données POST et l'instance du produit
         if form.is_valid():
             form.save()
             return redirect('product_list')
     else:
         form = ProductForm(instance=product)
     return render(request, 'shop/product_update.html', {'form': form})
 


def product_delete(request, pk):
     product = get_object_or_404(Product, pk=pk)
     if request.method == 'POST':
         product.delete()
         return redirect('product_list')
     return render(request, 'shop/product_delete.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# Lister les détails des commandes
def liste_details_commande(request):
    details = DetailCommande.objects.all()
    return render(request, "details_commandes/liste_details_commande.html", {"details": details})

# Ajouter un détail de commande
@login_required
def ajouter_details_commande(request):
    if request.method == "POST":
        form = DetailCommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("liste_details")
    else:
        form = DetailCommandeForm()
    return render(request, "details_commandes/ajouter_details_commande.html", {"form": form})



# ================= CLIENTS =================
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste_clients.html', {'clients': clients})

def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'clients/ajouter_client.html', {'form': form})

def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/ajouter_client.html', {'form': form})

def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('liste_clients')
def liste_commandes(request):
    commandes = Commande.objects.all()

    # Calculer le total pour chaque commande
    for commande in commandes:
        commande.calculer_total()

    return render(request, 'commandes/liste_commandes.html', {'commandes': commandes})

@login_required
def ajouter_commande(request):
     if request.method == 'POST':
         form = CommandeForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('liste_commandes')
     else:
         form = CommandeForm()
     return render(request, 'commandes/ajouter_commande.html', {'form': form})

def modifier_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('liste_commandes')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'commandes/ajouter_commande.html', {'form': form})

def supprimer_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    commande.delete()
    return redirect('liste_commandes')

def export_products_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow(["ID", "name", "descreption", "price", "stock","seul_alerte","fournisseur","categorie"])
    products = Product.objects.all()
    for product in products:
        writer.writerow([product.name, product.description, product.price, product.stock,product.seuil_alerte,product.fournisseur,product.categorie])
        
    return response
@login_required
@permission_required('shop.ajouter_paiement', raise_exception=True)
def ajouter_paiement(request, commande_id):
    # Récupérer la commande ou afficher une page d'erreur si elle n'existe pas
    commande = get_object_or_404(Commande, id=commande_id)

    if request.method == 'POST':
        try:
            # Validation des données de paiement
            montant = float(request.POST['montant'])  # Assurer que c'est un nombre
            mode_paiement = request.POST['mode_paiement']

            # Validation du montant et du mode de paiement
            if montant <= 0:
                raise ValueError("Le montant doit être supérieur à zéro.")
            
            if not mode_paiement:
                raise ValueError("Le mode de paiement est obligatoire.")

            # Créer l'instance de paiement
            paiement = Paiement.objects.create(
                commande=commande,
                montant=montant,
                mode_paiement=mode_paiement
            )

            # Créer la facture liée au paiement
            facture = Facture.objects.create(
                paiement=paiement,
                commande=commande,
                montant_total=montant,
                statut='payée'
            )

            # Générer la facture PDF
            facture_pdf = facture.generer_facture_pdf()  # Assurez-vous que cette méthode existe

            # Retourner la facture en réponse sous forme de PDF
            response = HttpResponse(facture_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'
            return response

        except ValueError as e:
            # En cas d'erreur de validation (par exemple, montant négatif ou vide)
            return render(request, 'paiements/ajouter_paiement.html', {
                'commande': commande, 'error': str(e)
            })

        except Exception as e:
            # Gestion générale des erreurs
            return render(request, 'paiements/ajouter_paiement.html', {
                'commande': commande, 'error': "Une erreur est survenue. Merci de réessayer."
            })

    # Si la méthode est GET, afficher le formulaire
    return render(request, 'paiements/ajouter_paiement.html', {'commande': commande})

@login_required
@permission_required('shop.view_paiement', raise_exception=True)
def liste_paiements(request):
    paiements = Paiement.objects.all()  # Ou filtrez selon les besoins
    commandes = Commande.objects.all()  # Vous récupérez toutes les commandes
    
    return render(request, 'paiements/liste_paiements.html', {'paiements': paiements, 'commandes': commandes})

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

# Ajouter un fournisseur
def ajouter_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseurs/ajouter_fournisseur.html', {'form': form})

# Modifier un fournisseur
def modifier_fournisseur(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/modifier_fournisseur.html', {'form': form})

# Supprimer un fournisseur
def supprimer_fournisseur(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    fournisseur.delete()
    return redirect('liste_fournisseurs')

def liste_livraisons(request):
     livraisons = Livraison.objects.all()
     return render(request, 'livraisons/liste_livraisons.html', {'livraisons': livraisons})
def ajouter_livraison(request):
    if request.method == 'POST':
         form = LivraisonForm(request.POST)
         if form.is_valid():
            form.save()
            return redirect('liste_livraisons')
    else:
         form = LivraisonForm()
    return render(request, 'livraisons/ajouter_livraison.html', {'form': form})

def carte_livraison(request, livraison_id):
     livraison = Livraison.objects.get(id=livraison_id)
    
     # Appel API Google Maps pour récupérer la localisation
     url = f"https://maps.googleapis.com/maps/api/geocode/json?address={livraison.adresse_livraison}&key={GOOGLE_MAPS_API_KEY}"
     response = requests.get(url).json()
    
     if response['status'] == 'OK':
         location = response['results'][0]['geometry']['location']
         latitude = location['lat']
         longitude = location['lng']
     else:
         latitude = longitude = None
    
     return render(request, 'livraisons/carte.html', {
         'livraison': livraison,
         'latitude': latitude,
         'longitude': longitude,
        'google_maps_api_key': GOOGLE_MAPS_API_KEY
     })

def retour_produit_create(request):
    if request.method == 'POST':
        form = RetourProduitForm(request.POST)
        if form.is_valid():
            retour = form.save(commit=False)
            
            # Vérification : est-ce que le produit figure bien dans la commande ?
            try:
                detail = DetailCommande.objects.get(commande=retour.commande, product=retour.product)
            except DetailCommande.DoesNotExist:
                messages.error(request, "Ce produit ne fait pas partie de la commande sélectionnée.")
                return render(request, 'retours/retour_produit_create.html', {'form': form})

            # Vérification : quantité retournée > quantité commandée ?
            if retour.quantite > detail.quantite:
                messages.error(request, f"La quantité retournée ({retour.quantite}) dépasse la quantité commandée ({detail.quantite}).")
                return render(request, 'retours/retour_produit_create.html', {'form': form})

            # Enregistrer le retour
            retour.save()

            # Diminuer la quantité dans DetailCommande
            detail.quantite -= retour.quantite
            detail.save()

            messages.success(request, "Retour enregistré et quantité mise à jour avec succès.")
            return redirect('liste_retours')
    else:
        form = RetourProduitForm()

    commandes = Commande.objects.all()
    return render(request, 'retours/retour_produit_create.html', {'form': form, 'commandes': commandes})
def liste_retours(request):
    retours = RetourProduit.objects.all()
    return render(request, 'retours/liste_retours.html', {'retours': retours})


def tableau_bord(request):
    total_products = Product.objects.count()
    total_orders = Commande.objects.count()
    total_clients = Client.objects.count()
    total_payments = Paiement.objects.count()

    orders_by_status = Commande.objects.values('statut').annotate(count=Count('statut'))
    payments_by_mode = Paiement.objects.values('mode_paiement').annotate(count=Count('mode_paiement'))
    product_categories = Product.objects.values('categorie').annotate(count=Count('categorie'))

    top_products_by_category = (
        Product.objects
        .values('categorie', 'name', 'price')
        .annotate(product_count=Count('commande'))
        .order_by('-product_count')
    )

    sales_by_date = Commande.objects.values('date').annotate(total_sales=Sum('total')).order_by('date')
    sales_data = {
        'date': [sale['date'] for sale in sales_by_date],
        'total_sales': [sale['total_sales'] for sale in sales_by_date],
    }
    df_sales = pd.DataFrame(sales_data)

    # --- Courbe évolution des ventes ---
    fig_sales_by_date = go.Figure()
    fig_sales_by_date.add_trace(go.Scatter(
        x=df_sales['date'],
        y=df_sales['total_sales'],
        mode='lines+markers',
        line=dict(color='rgba(255, 99, 71, 0.8)', width=4),  # Tomato orange
        marker=dict(size=10, color='rgba(255, 140, 0, 0.9)', line=dict(width=2, color='rgba(255, 69, 0, 1)'))
    ))
    fig_sales_by_date.update_layout(
        title="Évolution des Ventes",
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, title="Date"),
        yaxis=dict(showgrid=True, gridcolor='lightgrey', title="Total des ventes (€)"),
        font=dict(family="Arial, sans-serif", size=14, color="#333"),
        hovermode='x unified',
        transition = {'duration': 500, 'easing': 'cubic-in-out'}
    )

    # --- Histogramme des produits les plus commandés ---
    product_names = [f"{p['name']} ({p['categorie']})" for p in top_products_by_category]
    product_counts = [p['product_count'] for p in top_products_by_category]

    # Dégradé orange -> rouge pour les barres
    fig_bar_top_products = go.Figure(data=[go.Bar(
        x=product_names,
        y=product_counts,
        marker=dict(
            color=product_counts,
            colorscale='OrRd',
            line=dict(color='rgba(0,0,0,0.2)', width=1.5)
        ),
        hovertemplate="%{x}: %{y} commandes<extra></extra>"
    )])
    fig_bar_top_products.update_layout(
        title="Produits les Plus Commandés par Catégorie",
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        yaxis=dict(title="Nombre de commandes"),
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(b=150),
        transition = {'duration': 600, 'easing': 'cubic-in-out'}
    )

    # --- Pie chart : Répartition des produits ---
    products = Product.objects.all()
    fig_pie = go.Figure(data=[go.Pie(
        labels=[f"{p.name} - {p.categorie}" for p in products],
        values=[1 for _ in products],
        marker=dict(colors=px.colors.qualitative.Safe),
        hoverinfo='label+percent',
        textinfo='none'
    )])
    fig_pie.update_layout(
        title="Répartition des Produits par Catégorie",
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    # --- Bar chart : commandes par statut et client ---
    commandes = Commande.objects.select_related('client')
    statut_client_data = {}
    for commande in commandes:
        key = f"{commande.client.nom} - {commande.statut}"
        statut_client_data[key] = statut_client_data.get(key, 0) + 1

    fig_bar_orders = go.Figure(data=[go.Bar(
        x=list(statut_client_data.keys()),
        y=list(statut_client_data.values()),
        marker_color='rgba(255, 165, 0, 0.9)'  # Orange vif
    )])
    fig_bar_orders.update_layout(
        title="Commandes par Statut et par Client",
        xaxis_title="Client - Statut",
        yaxis_title="Nombre de Commandes",
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(b=150),
        transition = {'duration': 600, 'easing': 'cubic-in-out'}
    )

    # --- Pie chart : paiements par client ---
    paiements = Paiement.objects.select_related('commande__client')
    payment_labels = [f"{p.commande.client.nom} - {p.montant}€" for p in paiements]
    payment_values = [p.montant for p in paiements]

    fig_pie_payments = go.Figure(data=[go.Pie(
        labels=payment_labels,
        values=payment_values,
        marker=dict(colors=px.colors.qualitative.Pastel),
        hoverinfo='label+percent+value',
        textinfo='percent+label'
    )])
    fig_pie_payments.update_layout(
        title="Paiements par Client",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    # --- Pie chart : paiements par mode ---
    paiements_par_mode = Paiement.objects.values('mode_paiement').annotate(total=Sum('montant'))
    fig_pie_modes = go.Figure(data=[go.Pie(
        labels=[p['mode_paiement'] for p in paiements_par_mode],
        values=[p['total'] for p in paiements_par_mode],
        marker=dict(colors=px.colors.qualitative.Vivid),
        hoverinfo='label+percent+value',
        textinfo='percent+label'
    )])
    fig_pie_modes.update_layout(
        title="Répartition des Paiements par Mode",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_clients': total_clients,
        'total_payments': total_payments,
        'fig_pie': fig_pie.to_html(full_html=False),
        'fig_bar_orders': fig_bar_orders.to_html(full_html=False),
        'fig_pie_payments': fig_pie_payments.to_html(full_html=False),
        'fig_pie_modes': fig_pie_modes.to_html(full_html=False),
        'fig_bar_top_products': fig_bar_top_products.to_html(full_html=False),
        'fig_sales_by_date': fig_sales_by_date.to_html(full_html=False),
    }

    return render(request, 'shop/accueil.html', context)
def base_generic(request):
    return render(request, 'shop/base_generic.html')

def export_sales_report_to_excel(request):
    ventes = Commande.objects.all()
    
    # Créez un DataFrame avec les données
    data = {
        "ID Commande": [vente.id for vente in ventes],
        "Client": [vente.client.nom for vente in ventes],
        "Total": [vente.total for vente in ventes],
    }
    df = pd.DataFrame(data)
    
    # Exporter en Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="rapport_ventes.xlsx"'
    df.to_excel(response, index=False)
    
    return response

def liste_promotions(request):
    promotions = Promotion.objects.all()
    return render(request, 'promotions/liste.html', {'promotions': promotions})

def ajouter_promotion(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_promotions')
    else:
        form = PromotionForm()
    return render(request, 'promotions/ajouter.html', {'form': form})


def generer_inventaire_excel():
    produits = Product.objects.select_related('fournisseur').all()

    data = []
    for produit in produits:
        data.append({
            'Nom': produit.name,
            'Description': produit.description,
            'Catégorie': produit.categorie,
            'Fournisseur': produit.fournisseur.nom,  # Assure-toi que ton modèle Fournisseur a un champ 'nom'
            'Quantité en stock': produit.stock,
            'Seuil d\'alerte': produit.seuil_alerte,
            'Stock insuffisant': 'Oui' if produit.stock_insuffisant() else 'Non',
            'Prix unitaire': float(produit.price),
            'Valeur totale': float(produit.price) * produit.stock,
        })

    df = pd.DataFrame(data)

    # Créer le répertoire de stockage s'il n'existe pas
    dossier = 'media/inventaires'
    os.makedirs(dossier, exist_ok=True)

    # Nom du fichier avec date
    nom_fichier = f'inventaire_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.xlsx'
    chemin_fichier = os.path.join(dossier, nom_fichier)

    # Générer le fichier Excel
    df.to_excel(chemin_fichier, index=False)

    return chemin_fichier


from datetime import date, datetime
from datetime import datetime, timedelta


def liste_inventaires(request):
    produits = Product.objects.select_related('fournisseur').all()

    valeur_totale_inventaire = 0
    produits_data = []

    for p in produits:
        valeur = p.stock * p.price
        valeur_totale_inventaire += valeur
        produits_data.append({
            'nom': p.name,
            'stock': p.stock,
            'seuil_alerte': p.seuil_alerte,
            'fournisseur': p.fournisseur.nom,
            'prix': p.price,
            'valeur': valeur
        })

    context = {
        'produits': produits_data,
        'valeur_totale_inventaire': valeur_totale_inventaire,
        'today': date.today()
    }

    return render(request, 'inventaires/liste.html', context)

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_page(request):
    return render(request, 'payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

def create_checkout_session(request):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'xaf',
                    'product_data': {
                        'name': 'Paiement de produit',
                    },
                    'unit_amount': 1000 * 100,  # 1000 FCFA (en centimes)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})


from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        'Test Email depuis Django',
        'Ceci est un email de test pour vérifier la configuration Gmail.',
        'vanellemarceau025@gmail.com',  # expéditeur
        ['destinataire@gmail.com'],  # destinataire (mets ton adresse ici)
        fail_silently=False,
    )
    return HttpResponse("Email envoyé avec succès !")
