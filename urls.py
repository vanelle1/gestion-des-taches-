from django.shortcuts import render
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import login_view,base,ma_vue



urlpatterns = [
    path('shop/', views.login, name='login'),
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('base/', views.base, name='base'),
    path('home1/', views.home1, name='home1'),
    path('base_generic/', views.base_generic, name='base_generic'),
    path('accueil/', views.tableau_bord, name='accueil'),
    path('login/', login_view, name='login'), 
    path('', ma_vue, name='product_list'),
    path('promotions/', views.liste_promotions, name='liste_promotions'),
    path('promotions/ajouter/', views.ajouter_promotion, name='ajouter_promotion'),
    path('retours/', views.liste_retours, name='liste_retours'),  
    path('retour/ajouter/', views.retour_produit_create, name='retour_produit_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/modifier/<int:id>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:id>/', views.supprimer_client, name='supprimer_client'),
    path('commandes/', views.liste_commandes, name='liste_commandes'),
    path('commandes/ajouter/', views.ajouter_commande, name='ajouter_commande'),
    path('commandes/modifier/<int:id>/', views.modifier_commande, name='modifier_commande'),
    path('commandes/supprimer/<int:id>/', views.supprimer_commande, name='supprimer_commande'),
    path('details_commandes/', views.liste_details_commande, name='liste_details'),
    path('details_commandes/ajouter/', views.ajouter_details_commande, name='ajouter_details_commande'),
    
    path('livraisons/', views.liste_livraisons, name='liste_livraisons'),
    path('livraisons/carte/<int:livraison_id>/', views.carte_livraison, name='carte_livraison'),
    path('livraisons/ajouter/', views.ajouter_livraison, name='ajouter_livraison'),
    path("export/products/", views.export_products_csv, name="export_products_csv"),
    # path('livraisons/', views.liste_livraisons, name='liste_livraisons'),
    # path('livraisons/ajouter/', views.ajouter_livraison, name='ajouter_livraison'),
    path('ajouter_paiement/<int:commande_id>/', views.ajouter_paiement, name='ajouter_paiement'),
    path('liste_paiements/', views.liste_paiements, name='liste_paiements'),
   


    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('fournisseurs/ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('fournisseurs/modifier/<int:pk>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('fournisseurs/supprimer/<int:pk>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('inventaires/', views.liste_inventaires, name='liste_inventaires'),
     path('payer/', views.payment_page, name='payer'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', lambda r: render(r, 'success.html'), name='success'),
    path('cancel/', lambda r: render(r, 'cancel.html'), name='cancel'),
    path('logout/', LogoutView.as_view(), name='logout'),
   path('test-email/', views.test_email, name='test_email'),
   
   
    
]

