from django.db import models

class Bien(models.Model):
    Titre = models.CharField(max_length=200)
    Adresse = models.CharField(max_length=300)
    Description = models.TextField()
    Prix = models.DecimalField(max_digits=10, decimal_places=2)
    Type = models.CharField(max_length=100)
    Statut = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Titre 
STATUT_CHOICES = [
    ('Disponible', 'Disponible'),
    ('Loué', 'Loué'),
]
    

class ImageBien(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='biens/')
    
    def __str__(self):
        return f"Image for {self.bien.Titre}"    

# Create your models here.
