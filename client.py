from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_objet_or_404
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import requests
import argparse

# Endpoint: GET /datasets/
def list_datasets(request):
    datasets = Dataset.objects.all()
    datasets_list = []
    for k in datasets:
        datasets_list({'id' : k.id, 'filename' : k.filename, 'taille' : k.size})
    return HttpResponse(datasets_list)

# Endpoint: POST /datasets/
def create_dataset(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        dataset = dataset.object.create(filename = file.name, size = file.size)
        df = pd.read_csv(file)
        return HttpResponse({'id': dataset.id, 'url': f'/datasets/{dataset.id}/'})
    else:
        return HttpResponse({'error': 'Invalid request'})

# Endpoint: GET /datasets/<id>/
def get_dataset(request, id):
    dataset = get_objet_or_404(Dataset, id = id)
    return HttpReponse({'file' : dataset.filename, 'taille': dataset.size})

# Endpoint: DELETE /datasets/<id>/
def delete_dataset(requete, id):
    dataset = Dataset.objects.get_or_404(Dataset, id = id)
    dataset.delete()
    return HttpResponse({'message': 'Dataset supprimé'})

# Endpoint: GET /datasets/<id>/excel
def export_dataset_excel(request, id):
    dataset = get_objet_or_404(Dataset, id = id)
    df = pd.read_csv(dataset.filepath)
    excel_file = df.to_excel(index=False)
    response = HttpResponse()
    excel_file.save(response)
    return response

# Endpoint: GET /datasets/<id>/stats/
def get_dataset_stats(request, id):
    dataset = get_objet_or_404(Dataset, id = id)
    df = pd.read_csv(dataset.filepath)
    stat = df.describe().to_dict()
    return HttpResponse(stat)



def generate_dataset_plot(request, id):
    dataset = Dataset.objects.filter(id=id).first()
    if not dataset:
        return HttpResponse({'error': 'Dataset not found'}, status=404)
    df = pd.read_csv(dataset.filepath)
    figsize=(8, 6*len(df.columns))
    fig, axs = plt.subplots(len(df.columns), 1, figsize)
    for i, column in enumerate(df.columns):
        axs[i].hist(df[column])
        axs[i].set_title(column)
        
    pdf_filename = "dataset_plot.pdf"
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig)
    with open(pdf_filename, 'rb') as file:
        return HttpResponse(file.read())

import argparse

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
    reponse = requests.get(url)
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

