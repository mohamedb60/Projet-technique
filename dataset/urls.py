from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_datasets, name='list_datasets'),
    path('create/', views.create_dataset, 
name='create_dataset'),
    path('<int:id>/', views.get_dataset, name='get_dataset'),
    path('<int:id>/delete/', views.delete_dataset, 
name='delete_dataset'),
    path('<int:id>/excel/', views.export_dataset_excel, 
name='export_dataset_excel'),
    path('<int:id>/stats/', views.get_dataset_stats, 
name='get_dataset_stats'),
    path('<int:id>/plot/', views.generate_dataset_plot, 
name='generate_dataset_plot'),
]

