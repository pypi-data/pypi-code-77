from django.db import models
from django.urls.base import reverse
from djangosimplemodels import SimpleAddress

# Create your models here.

class Region(models.Model):

    class Meta:
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'

    name = models.CharField(
        verbose_name="Nome", 
        max_length=254
    )

    acronym = models.CharField(
        verbose_name="Sigla", 
        max_length=2
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("region_detail", kwargs={"pk": self.pk})


class State(models.Model):

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    name = models.CharField(
        verbose_name="Nome", 
        max_length=254
    )

    acronym = models.CharField(
        verbose_name="Sigla", 
        max_length=2
    )

    region = models.ForeignKey(
        "Region", 
        verbose_name="Região", 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("state_detail", kwargs={"pk": self.pk})


class City(models.Model):

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

    name = models.CharField(
        verbose_name="Nome", 
        max_length=254
    )

    state = models.ForeignKey(
        "State", 
        verbose_name="", 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("city_detail", kwargs={"pk": self.pk})


class Address(SimpleAddress):

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    zipcode = models.CharField(
        verbose_name="CEP",
        max_length=8,
        blank=True,
        null=True
    )

    state = models.ForeignKey(
        "State", 
        verbose_name="Estado", 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    city = models.ForeignKey(
        "City", 
        verbose_name="Município", 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    district = models.CharField(
        verbose_name="Bairro",
        max_length=254
    )

    address = models.CharField(
        verbose_name="Endereço",
        max_length=254
    )

    number = models.IntegerField(
        verbose_name="Número",
    )

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("address_detail", kwargs={"pk": self.pk})
