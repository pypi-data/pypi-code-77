from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_model import models as edc_models
from edc_reportable.model_mixin import BloodResultsModelMixin
from respond_model.model_mixins import BloodResultsFbcModelMixin


class BloodResultsFbc(
    BloodResultsFbcModelMixin,
    CrfNoManagerModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(CrfNoManagerModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: FBC"
        verbose_name_plural = "Blood Results: FBC"
