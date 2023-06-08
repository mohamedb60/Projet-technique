from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_objet_or_404
import pandas as pd


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

