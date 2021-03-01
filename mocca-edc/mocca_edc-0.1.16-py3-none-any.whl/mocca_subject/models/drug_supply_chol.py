from django.db import models
from edc_model import models as edc_models

from mocca_lists.models import CholTreatments

from .drug_refill_chol import DrugRefillChol


class DrugSupplyChol(edc_models.BaseUuidModel):

    drug_refill = models.ForeignKey(DrugRefillChol, on_delete=models.PROTECT)

    drug = models.ForeignKey(CholTreatments, on_delete=models.PROTECT)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Drug Supply: Hypertension"
        verbose_name_plural = "Drug Supply: Hypertension"
