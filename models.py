# © 2025 Tagang Vanelle
# Licensed under the MIT License – See LICENSE file for details

import datetime
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
# shop/models.py

class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    adresse = models.TextField()
    email = models.EmailField()
    prix_contrat = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    categorie_produit = models.CharField(max_length=255, default="Non défini")  
    date = models.DateField(default=timezone.now)  

    def __str__(self):
        return self.nom
class Client(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    email = models.EmailField()
    adresse = models.TextField()
    historique_achats = models.JSONField(default=list)

    def __str__(self):
        return self.nom
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.CharField(max_length=255, blank=True, null=True) 
    seuil_alerte = models.PositiveIntegerField(default=10)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    CATEGORIES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Food', 'Food'),
        ('Furniture', 'Furniture'),
        ('Depot', 'Dépôt'), 
        ('Supermarché', 'Supermarché'),  
    ]
    
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='Electronics')

    def __str__(self):
        return self.name

    def stock_insuffisant(self):
        return self.stock <= self.seuil_alerte
         
class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    statut = models.CharField(
        max_length=50,
        choices=[('En attente', 'En attente'), ('En cours', 'En cours'), ('Livrée', 'Livrée')],
        default='En attente'
    )
    product = models.ManyToManyField(Product, through='DetailCommande')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def calculer_total(self):
     if self.total == 0:  # Vérifier si le total a déjà été calculé
        total = sum(item.product.price * item.quantite for item in self.details.all())
        self.total = total
        self.save()
    def save(self, *args, **kwargs):
        """Override de la méthode save pour recalculer le total avant d'enregistrer"""
        self.calculer_total()  # Recalcule le total chaque fois que la commande est enregistrée
        super().save(*args, **kwargs)
    def annuler_commande_si_retour_complet(self):
        # Quantité totale commandée
        quantite_commandee = sum(detail.quantite for detail in self.details.all())

        # Quantité totale retournée (retours approuvés liés à cette commande)
        quantite_retournee = sum(retour.quantite for retour in self.retourproduit_set.filter(statut='Approuvé'))

        if quantite_retournee >= quantite_commandee:
            self.statut = 'Annulée'
            self.save()

    def __str__(self):
        return f"Commande #{self.id} - {self.client}"


        
class DetailCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name="details", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.product.name} (Commande #{self.commande.id})"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si c'est un nouvel enregistrement
            if self.product.stock >= self.quantite:
                self.product.stock -= self.quantite
                self.product.save()
            else:
                raise ValueError(f"Stock insuffisant pour le produit : {self.product.name}")
        super().save(*args, **kwargs)
        
class login(models.Model):
     username= models.CharField(max_length=100)
     password= models.CharField(max_length=100)
     
     
class MaVue(LoginRequiredMixin, TemplateView):
    template_name = 'add_product.html'
    

class Paiement(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(default=timezone.now)
    mode_paiement = models.CharField(
        max_length=20, 
        choices=[('espece', 'Espèce'), ('Carte', 'Carte Bancaire'), ('Mobile Money', 'Mobile Money')],
        default='espece'
    )

    def save(self, *args, **kwargs):
        # Utiliser automatiquement le total de la commande
        if self.commande and self.commande.total:
            self.montant = self.commande.total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Paiement {self.id} - {self.montant}€ pour {self.commande}"
    
class Livraison(models.Model):
     STATUT_CHOICES = [
         ('en_cours', 'En cours'),
         ('livré', 'Livré'),
         ('annulé', 'Annulé'),
    ]
    
     destinataire = models.CharField(max_length=255)
     adresse_livraison = models.CharField(max_length=255)
     statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
     date_creation = models.DateTimeField(auto_now_add=True)
    
     def __str__(self):
         return f"Livraison pour {self.destinataire} - {self.statut}"
class Facture(models.Model):
    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE)  # Lier une facture à un paiement
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    date_facture = models.DateField(default=timezone.now)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=[('payée', 'Payée'), ('non_payée', 'Non payée')], default='non_payée')

    def __str__(self):
        return f"Facture {self.id} - {self.montant_total}€ pour la commande {self.commande}"

    def generer_facture_pdf(self):
        """
        Génère un PDF pour la facture associée à la commande.
        """
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Informations de la facture
        p.drawString(100, 750, f"Facture - Commande #{self.commande.id}")
        p.drawString(100, 730, f"Date de Facture: {self.date_facture}")
        p.drawString(100, 710, f"Statut: {self.statut}")

        # Détails des produits dans la commande
        y = 680
        for detail in self.commande.details.all():
            produit = detail.product
            quantite = detail.quantite
            p.drawString(100, y, f"{produit.name} x {quantite} @ {produit.price} FCFA")
            y -= 20

        # Total de la commande
        p.drawString(100, y - 20, f"Total : {self.commande.total} FCFA")

        # Enregistrement du PDF
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer


class RetourProduit(models.Model):
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    motif = models.TextField()
    statut = models.CharField(
        max_length=50,
        choices=[
            ('En attente', 'En attente'),
            ('Approuvé', 'Approuvé'),
            ('Refusé', 'Refusé')
        ],
        default='En attente'
    )
    date_retour = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Retour de {self.product.name} - {self.quantite}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # toujours sauvegarder en premier

        if self.statut == 'Approuvé':
            self.commande.statut = 'Retour'
            self.commande.save()

            # Vérifie si tous les produits ont été retournés
            self.commande.annuler_commande_si_retour_complet()

            # Mise à jour du stock
            self.mettre_a_jour_stock()

    def mettre_a_jour_stock(self):
        self.product.stock += self.quantite
        self.product.save()

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reduction = models.DecimalField(max_digits=5, decimal_places=2, help_text="Réduction en pourcentage")
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name} - {self.reduction}%"

    def est_active(self):
        now = timezone.now()
        return self.date_debut <= now <= self.date_fin
