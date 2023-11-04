from django.db import models
from rest_framework.schemas import ManualSchema, coreapi


# Create your models here.

class Mahsulot_turi(models.Model):
    nom = models.CharField(max_length=150)

    def __str__(self):
        return self.nom


class Mahsulot(models.Model):
    nom = models.CharField(max_length=150)
    turi = models.ForeignKey(Mahsulot_turi, on_delete=models.SET_NULL, null=True)
    narx1 = models.FloatField()
    narx2 = models.FloatField(null=True, blank=True)
    miqdor = models.IntegerField()
    izoh = models.TextField(null=True, blank=True)
    sana = models.DateField()

    def __str__(self):
        return f"{self.nom} | {self.narx1}"


class Mijoz(models.Model):
    avtomobil = models.CharField(max_length=150, null=True, blank=True)
    avto_raqam = models.CharField(max_length=20, blank=True, null=True)
    # summa = models.FloatField()
    # sana = models.DateTimeField()

    def __str__(self):
        return f"{self.avto_raqam} | {self.avtomobil}"


class Savdo(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.SET_NULL, null=True)
    miqdor = models.IntegerField()
    summa = models.FloatField()
    mijoz = models.ForeignKey(Mijoz, on_delete=models.SET_NULL, null=True,
                              related_name="savdolar")
    sana = models.DateField()

    def __str__(self):
        return f"{self.mahsulot} | {self.miqdor}"


class Chiqim(models.Model):
    summa = models.FloatField()
    izoh = models.CharField(max_length=500)
    masul = models.CharField(max_length=200, blank=True, null=True)
    sana = models.DateField()

    def __str__(self):
        return f"{self.summa} | {self.izoh[:20]}"

