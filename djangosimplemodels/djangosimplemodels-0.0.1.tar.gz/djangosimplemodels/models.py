from abc import abstractclassmethod
from django.db import models

# Create your models here.

class SimpleModel(models.Model):

    class Meta:
        abstract = True

    description = models.CharField(
        "Descrição", 
        max_length=254
    )


class SimpleAddress(models.Model):

    class Meta:
        abstract = True
        

    zipcode = models.CharField(
        verbose_name="CEP",
        max_length=254,
        blank=True,
        null=True
    )

    state = models.CharField(
        verbose_name="Estado",
        max_length=254,
        blank=True,
        null=True
    )

    city = models.CharField(
        verbose_name="Município",
        max_length=254,
        blank=True,
        null=True
    )

    district = models.CharField(
        verbose_name="Bairro",
        max_length=254,
        blank=True,
        null=True
    )

    address = models.CharField(
        verbose_name="Endereço",
        max_length=254,
        blank=True,
        null=True
    )

    number = models.CharField(
        verbose_name="Número",
        max_length=254,
        blank=True,
        null=True
    )

    complement = models.CharField(
        verbose_name="Complemento",
        max_length=254,
        blank=True,
        null=True
    )


class SimpleVehicle(models.Model):
    
    class Meta:
        abstract = True
    
    manufacturer = models.CharField(
        verbose_name="Fabricante", 
        max_length=254,
        blank=True,
        null=True
    )

    model = models.CharField(
        verbose_name="Modelo", 
        max_length=254,
        blank=True,
        null=True
    )

    year = models.CharField(
        verbose_name="Ano",
        max_length=254,
        blank=True,
        null=True
    )

    board = models.CharField(
        verbose_name="Placa",
        max_length=254,
        blank=True,
        null=True
    )

    color = models.CharField(
        verbose_name="Cor",
        max_length=254,
        blank=True,
        null=True
    )

    km_current = models.CharField(
        verbose_name="KM Atual",
        max_length=254,
        blank=True,
        null=True
    )

    type_fuel = models.CharField(
        verbose_name="Combustível",
        max_length=254,
        blank=True,
        null=True
    )

    note = models.TextField(
        verbose_name="Observações",
        blank=True,
        null=True
    )