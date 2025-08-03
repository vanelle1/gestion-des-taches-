
from django.contrib import admin
from .models import Commande, DetailCommande, Fournisseur, Livraison, Paiement, Product, Client, Promotion, RetourProduit

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    search_fields=['name']
    fields=['price','stock','description']
    list_display=('name','price','stock','description')
    list_filter=['name','price']
    list_per_page=5
admin.site.register(Product,ProductAdmin) ## est utilisée pour enregistrer un modèle dans l'interface d'administration de Django

class CommandeAdmin(admin.ModelAdmin):
    search_fields=['client']
    list_display=('client','id','statut')
admin.site.register(Commande,CommandeAdmin)

class ClientAdmin(admin.ModelAdmin):
    search_fields=['nom']
    fields=['nom','contact','email']
    list_display=('nom','contact','email')
    list_filter=['nom','historique_achats']
    list_per_page=5
admin.site.register(Client,ClientAdmin)

class DetailCommandeAdmin(admin.ModelAdmin):
    search_fields=['commande']
    fields=['commande','product','quantite']
    list_display=('commande','product','quantite')
    list_filter=['product','quantite']
    list_per_page=5
admin.site.register(DetailCommande,DetailCommandeAdmin)

class LivraisonAdmin(admin.ModelAdmin):
   admin.site.register(Livraison)
   
class FournisseurAdmin(admin.ModelAdmin):
    search_fields=['nom']
    fields=['nom','contact','email']
    list_display=('nom','contact','email')
    list_filter=['nom']
    list_per_page=5
admin.site.register(Fournisseur,FournisseurAdmin)
class PaiementAdmin(admin.ModelAdmin):
    search_fields=['commande']
    fields=['commande','montant','mode_paiement']
    list_display=('commande','montant')
    list_filter=['commande','mode_paiement']
    list_per_page=5
admin.site.register(Paiement,PaiementAdmin)
class RetourProduitAdmin(admin.ModelAdmin):
    search_fields=['motif']
    fields=['commande','product','statut']
    list_display=('commande','product','motif')
    list_filter=['commande','statut']
    list_per_page=5
admin.site.register(RetourProduit,RetourProduitAdmin)

class PromotionAdmin(admin.ModelAdmin):
    list_display = ( 'reduction', 'date_debut', 'date_fin', 'est_active')
    list_filter = ('date_debut', 'date_fin')
    
admin.site.register(Promotion,PromotionAdmin)