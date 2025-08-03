from django import forms
from .models import Paiement, Product, Client, Commande, Fournisseur, Promotion, RetourProduit
from .models import DetailCommande
from .models import Livraison

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'contact', 'adresse', 'email','prix_contrat','categorie_produit']
        
class ProductForm(forms.ModelForm):  # Correction ici
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'description', 'image', 'seuil_alerte', 'fournisseur','categorie']
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'contact', 'email', 'adresse', 'historique_achats']
        
class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['client', 'statut', 'product','total']

    def save(self, commit=True):
        commande = super().save(commit=False)
        if commit:
            commande.save()
        # Calculer le total de la commande
        commande.calculer_total()
        return commande
       
class DetailCommandeForm(forms.ModelForm):
    class Meta:
        model = DetailCommande
        fields = ['commande', 'product', 'quantite']  

class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['destinataire','adresse_livraison','statut']


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['commande', 'montant', 'mode_paiement']
    
    def __init__(self, *args, **kwargs):
        super(PaiementForm, self).__init__(*args, **kwargs)
        
        # Rendre la commande en lecture seule (désactiver le champ)
        if 'commande' in self.fields:
            self.fields['commande'].disabled = True
        
        # Rendre le champ montant en lecture seule
        if 'montant' in self.fields:
            self.fields['montant'].disabled = True  # Lecture seule




class RetourProduitForm(forms.ModelForm):
    class Meta:
        model = RetourProduit
        fields = ['commande', 'product', 'quantite', 'motif','statut']

    def __init__(self, *args, **kwargs):
     super(RetourProduitForm, self).__init__(*args, **kwargs)
    
    # Vérifie si la commande est bien sélectionnée
     if 'commande' in self.data:
        try:
            commande_id = int(self.data.get('commande'))
            # Filtrer les produits associés à la commande
            products = DetailCommande.objects.filter(commande_id=commande_id).values_list('product', flat=True)
            self.fields['product'].queryset = Product.objects.filter(id__in=products)
        except (ValueError, TypeError):
            pass
     elif self.instance.pk:
        # Si c'est une instance existante, utilise la commande de l'instance
        self.fields['product'].queryset = self.instance.commande.detailcommande_set.all().values_list('product', flat=True)

    # Ajout de classes CSS pour l'apparence
     self.fields['commande'].widget.attrs.update({'class': 'form-control'})
     self.fields['product'].widget.attrs.update({'class': 'form-control'})
     self.fields['quantite'].widget.attrs.update({'class': 'form-control'})
     self.fields['motif'].widget.attrs.update({'class': 'form-control'})
        
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['product', 'reduction', 'date_debut', 'date_fin']
