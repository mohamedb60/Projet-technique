from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_objet_or_404
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Endpoint: GET /datasets/
def liste_datasets(requete):
   datasets = Datasets.objects.all()
   liste_datasets = []
   for k in datasets:
      liste_datasets('id' : k.id, 'nom_fichier' : k.filename, 'taille' : dataset.size)
   return HttpResponse(liste_datasets)

# Endpoint: POST /datasets/
def create_dataset(requete):
    if requete.method == 'POST' and request.FILES.get('fichier'):
	fichier = requete.FILES['fichier']
	dataset = dataset.object.create(fichier_nom = fichier.name, taille = fichier.size)
	df = pd.read_csv(fichier)
        return HttpResponse({'id': dataset.id, 'url': f'/datasets/{dataset.id}/'})
    else:
        return HttpResponse({'error': 'Invalid request'})

# Endpoint: GET /datasets/<id>/
def get_dataset(requete, id):
   dataset = get_objet_or_404(Dataset, id = id)
   return HttpReponse({'fichier' : dataset.filename, 'taille': dataset.size})

# Endpoint: DELETE /datasets/<id>/
def delete_dataset(requete, id):
   dataset = Dataset.objects.get_or_404(Dataset, id = id)
        dataset.delete()
        return HttpResponse({'message': 'Dataset supprimé'})

# Endpoint: GET /datasets/<id>/excel
def export_dataset_excel(requete, id):
    dataset = get_object_or_404(Dataset, id=id)
    df = pd.read_csv(dataset.filepath)
    excel_file = df.to_excel(index=False)
    reponse = HttpResponse()
    excel_file.save(reponse)
    return reponse

# Endpoint: GET /datasets/<id>/stats/
def get_dataset_stats(requete, id):
    dataset = get_object_or_404( Dataset, id=id)
    df = pd.read_csv(dataset.filepath)
    stat = df.describe().to_dict()
    return HttpResponse(stat)



def generate_dataset_plot(requete, id):
    dataset = Dataset.objects.filter(id=id).first()
    if not dataset:
        return HttpResponse({'error': 'Dataset not found'}, status=404)
 df = pd.read_csv(dataset.filepath)
    fig, axs = plt.subplots(len(df.columns), 1, figsize=(8, 6*len(df.columns)))
    for i, column in enumerate(df.columns):
        axs[i].hist(df[column])
        axs[i].set_title(column)
    pdf_filename = "dataset_plot.pdf"
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig)
    with open(pdf_filename, 'rb') as file:
        reponse = HttpResponse(file.read())
        return reponse
