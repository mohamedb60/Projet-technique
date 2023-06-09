from .models import Dataset
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Endpoint: GET /datasets/
def list_datasets(request):
    datasets = Dataset.objects.all()
    datasets_list = []
    for k in datasets:
        datasets_list.append({'id': k.id, 'filename': k.filename, 'size': k.size})
    return HttpResponse(datasets_list)

# Endpoint: POST /datasets/
def create_dataset(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        dataset = object.create(filename = file.name, size = file.size)
        df = pd.read_csv(file)
        return HttpResponse({'id': dataset.id, 'url': f'/datasets/{dataset.id}/'})
    else:
        return HttpResponse({'error': 'Invalid request'})

# Endpoint: GET /datasets/<id>/
def get_dataset(request, id):
    dataset = get_object_or_404(Dataset, id = id)
    return HttpResponse({'file' : dataset.filename, 'size': dataset.size})

# Endpoint: DELETE /datasets/<id>/
def delete_dataset(request, id):
    dataset = Dataset.object.get_or_404(Dataset, id = id)
    dataset.delete()
    return HttpResponse({'message': 'Dataset supprimé'})

# Endpoint: GET /datasets/<id>/excel
def export_dataset_excel(request, id):
    dataset = get_object_or_404(Dataset, id=id)
    df = pd.read_csv(dataset.filepath)
    excel_file = df.to_excel(index=False)
    response = HttpResponse()
    df.to_excel(response, index=False)
    return response

# Endpoint: GET /datasets/<id>/stats/
def get_dataset_stats(request, id):
    dataset = get_object_or_404( Dataset, id=id)
    df = pd.read_csv(dataset.filepath)
    stat = df.describe().to_dict()
    return HttpResponse(stat)



def generate_dataset_plot(request, id):
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
        return HttpResponse(file.read())
    
    
