from django.db import models

class Dataset(models.Model):
    fichier_nom = models.CharField(max_length=255)
    taille = models.IntegerField()

    def __str__(self):
        return self.fichier_nom

