from django.conf import settings
from django.db import models

from ...stubs import ClinicalReviewModelStub


class ClinicalReviewModelMixin(models.Model):

    diagnoses_labels = settings.RESPOND_DIAGNOSIS_LABELS

    def get_best_test_date(self: ClinicalReviewModelStub, prefix: str):
        return getattr(self, f"{prefix}_test_date", None) or getattr(
            self, f"{prefix}_test_estimated_datetime", None
        )

    @property
    def diagnoses(self: ClinicalReviewModelStub) -> dict:
        return {k: getattr(self, f"{k}_dx") for k in self.diagnoses_labels}

    class Meta:
        abstract = True
