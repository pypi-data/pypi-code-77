from edc_model import models as edc_models
from edc_visit_schedule.constants import DAY1
from respond_model.model_mixins import (
    ClinicalReviewBaselineCholModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewModelMixin,
)

from ..model_mixins import CrfModelMixin


class ClinicalReviewBaselineError(Exception):
    pass


class ClinicalReviewBaseline(
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineCholModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    def save(self, *args, **kwargs):
        if (
            self.subject_visit.visit_code != DAY1
            and self.subject_visit.visit_code_sequence != 0
        ):
            raise ClinicalReviewBaselineError(
                f"This model is only valid at baseline. Got `{self.subject_visit}`."
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Review: Baseline"
        verbose_name_plural = "Clinical Review: Baseline"
