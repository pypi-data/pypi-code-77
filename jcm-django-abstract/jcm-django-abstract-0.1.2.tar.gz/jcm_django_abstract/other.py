from django.db import models


class AbstractStringPK(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    class Meta:
        abstract = True


class AbstractOrdering(models.Model):
    default_order = models.IntegerField(default=0)

    class Meta:
        abstract = True
