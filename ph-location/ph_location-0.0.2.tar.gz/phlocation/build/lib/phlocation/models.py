from django.db import models
from django.db.models import Q


class PSGCManager(models.Manager):
    def regions(self):
        return self.get_queryset().filter(geographic_level=PSGC.REGION)

    def all_districts_provinces(self):
        return self.get_queryset().filter(
            Q(geographic_level=PSGC.DISTRICT) |
            Q(geographic_level=PSGC.PROVINCE) |
            Q(geographic_level=PSGC.EMPTY)
        )

    def districts_provinces(self, region_code):
        return self.get_queryset().filter(
            code__gt=region_code,
            code__lt=region_code + 10000000
        ).filter(
            Q(geographic_level=PSGC.DISTRICT) |
            Q(geographic_level=PSGC.PROVINCE) |
            Q(geographic_level=PSGC.EMPTY)
        )

    def all_cities_municipalities(self):
        return self.get_queryset().filter(
            Q(geographic_level=PSGC.CITY) |
            Q(geographic_level=PSGC.MUNICIPALITY) |
            Q(geographic_level=PSGC.SUB_MUNICIPALITY)
        )

    def cities_municipalities(self, province_code):
        return self.get_queryset().filter(
            code__gt=province_code,
            code__lt=province_code + 100000
        ).filter(
            Q(geographic_level=PSGC.CITY) |
            Q(geographic_level=PSGC.MUNICIPALITY) |
            Q(geographic_level=PSGC.SUB_MUNICIPALITY)
        )

    def all_barangays(self):
        return self.get_queryset().filter(
            geographic_level=PSGC.BARANGAY,
        )

    def barangays(self, municipality_code):
        return self.get_queryset().filter(
            code__gt=municipality_code,
            code__lt=municipality_code + 1000,
            geographic_level=PSGC.BARANGAY,
        )


class PSGC(models.Model):
    class Meta:
        verbose_name_plural = 'psgc'

    objects = PSGCManager()

    REGION = 'Reg'

    PROVINCE = 'Prov'
    DISTRICT = 'Dist'
    EMPTY = 'Empty'

    CITY = 'City'
    MUNICIPALITY = 'Mun'
    SUB_MUNICIPALITY = 'SubMun'

    BARANGAY = 'Bgy'

    GEOGRAPHIC_LEVEL_CHOICES = (
        (REGION, 'Region'),
        (PROVINCE, 'Province'),
        (DISTRICT, 'District'),
        (EMPTY, 'Empty'),
        (CITY, 'City'),
        (MUNICIPALITY, 'Municipality'),
        (SUB_MUNICIPALITY, 'Sub Municipality'),
        (BARANGAY, 'Barangay'),
    )

    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    geographic_level = models.CharField(max_length=6, choices=GEOGRAPHIC_LEVEL_CHOICES)

    def __str__(self):
        # return f"{self.code:09} {self.name}"
        return self.name
