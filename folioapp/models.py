from django.db import models

# Create your models here.

class Monedas(models.Model):
    moneda = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=255)
    precio = models.FloatField(blank=True, null=True)


class Proyects(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=1000)
    def __str__(self):
        return self.titulo

class ProyectImg(models.Model):
    proyecto = models.ForeignKey(Proyects, on_delete=models.CASCADE)
    imgList = models.ImageField()
    imgDescript = models.CharField(max_length=255)
