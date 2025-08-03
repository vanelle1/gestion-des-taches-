import csv
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
django.setup()

from shop.models import Product  

# Exportation en CSV
with open("Product.csv", "w", newline="", encoding="utf-8") as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(["ID", "name","description","Price","stock","seuil-alerte","fournisseur","categorie"])  # En-têtes

    for produit in Product.objects.all():
        writer.writerow([ Product.name, Product.description,Product.price,Product.stock,Product.seuil_alerte,Product.fournisseur,Product.categorie])

print("Exportation terminée !")
