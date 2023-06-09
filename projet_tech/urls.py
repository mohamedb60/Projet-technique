"""
URL configuration for projet_tech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.list_datasets, name='list_datasets'),
    path('create/', views.create_dataset, name='create_dataset'),
    path('<int:id>/', views.get_dataset, name='get_dataset'),
    path('<int:id>/delete/', views.delete_dataset, name='delete_dataset'),
    path('<int:id>/excel/', views.export_dataset_excel, name='export_dataset_excel'),
    path('<int:id>/stats/', views.get_dataset_stats, name='get_dataset_stats'),
    path('<int:id>/plot/', views.generate_dataset_plot, name='generate_dataset_plot'),
]
