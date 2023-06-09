from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import requests
import argparse
from .models import Dataset


BASE_URL = "http://127.0.0.1:8000/"  

def list_datasets():
    url = f"{BASE_URL}/datasets/"
    response = requests.get(url)
    if response.status_code == 200:
        datasets = response.json()
        for dataset in datasets:
            print(dataset["filename"])
    else:
        print("Erreur lors de la récupération de la liste des datasets.")

def create_dataset(csv_file):
    url = f"{BASE_URL}/datasets/"
    files = {"file": open(csv_file, "rb")}
    response = requests.post(url, files=files)
    if response.status_code == 201:
        dataset = response.json()
        print(f"Dataset créé avec l'ID : {dataset['id']}")
    else:
        print("Erreur lors de la création du dataset.")

def get_dataset_info(id):
    url = f"{BASE_URL}/datasets/{id}/"
    response = requests.get(url)
    if response.status_code == 200:
        dataset = response.json()
        print(f"Nom du file : {dataset['filename']}")
        print(f"Taille du file : {dataset['size']} bytes")
    else:
        print("Erreur lors de la récupération des informations du dataset.")


def delete_dataset(id):
    url = f"{BASE_URL}/datasets/{id}/"
    response = requests.delete(url)
    if response.status_code == 204:
        print("Dataset supprimé avec succès.")
    else:
        print("Erreur lors de la suppression du dataset.")

def export_dataset_excel(id):
    url = f"{BASE_URL}/datasets/{id}/excel/"
    response = requests.get(url)
    if response.status_code == 200:
        with open("dataset.xlsx", "wb") as file:
            file.write(response.content)
        print("Dataset exporté en format Excel.")
    else:
        print("Erreur lors de l'exportation du dataset en format Excel.")

def get_dataset_stats(id):
    url = f"{BASE_URL}/datasets/{id}/stats/"
    response = requests.get(url)
    if response.status_code == 200:
        stats = response.json()
        print(stats)
    else:
        print("Erreur lors de la récupération des statistiques du dataset.")

def generate_dataset_plot(id):
    url = f"{BASE_URL}/datasets/{id}/plot/"
    response = requests.get(url)
    if response.status_code == 200:
        with open("dataset_plot.pdf", "wb") as file:
            file.write(response.content)
        print("Graphique généré et enregistré sous dataset_plot.pdf.")
    else:
        print("Erreur lors de la génération du graphique du dataset.")

# Créez un objet ArgumentParser
parser = argparse.ArgumentParser(description='application client')

# Définissez les arguments de ligne de commande
parser.add_argument('--list', action='store_true', help='List all datasets')
parser.add_argument('--create', type=str, help='Create a new dataset')
parser.add_argument('--delete', type=int, help='Delete a dataset by ID')
parser.add_argument('--excel', type=int, help='Export a dataset as an Excel file by ID')
parser.add_argument('--stats', type=int, help='Get statistics of a dataset by ID')
parser.add_argument('--plot', type=int, help='Generate a plot of a dataset by ID')

# Analysez les arguments de ligne de commande
args = parser.parse_args()

# Utilisez les arguments pour déterminer quelle action exécuter
if args.list:
    # Action pour lister les datasets
    list_datasets()
elif args.create:
    # Action pour créer un nouveau dataset
    create_dataset(args.create)
elif args.delete:
    # Action pour supprimer un dataset par ID
    delete_dataset(args.delete)
elif args.excel:
    # Action pour exporter un dataset en tant que fichier Excel par ID
    export_dataset_excel(args.excel)
elif args.stats:
    # Action pour obtenir les statistiques d'un dataset par ID
    get_dataset_stats(args.stats)
elif args.plot:
    # Action pour générer un graphique d'un dataset par ID
    generate_dataset_plot(args.plot)
else:
    # Aucune action spécifiée, affichez un message d'aide
    parser.print_help()







