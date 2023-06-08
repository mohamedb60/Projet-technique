from django.db import models

class Dataset(models.Model):
    nom_fichier = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_fichier
