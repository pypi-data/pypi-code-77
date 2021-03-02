from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_model.form_validators import (
    CrfFormValidatorMixin,
    GlucoseFormValidatorMixin,
    ResultFormValidatorMixin,
)
from respond_model.utils import (
    raise_if_clinical_review_does_not_exist,
    raise_if_not_baseline,
)

from ..models import Glucose


class GlucoseBaselineFormValidator(
    ResultFormValidatorMixin,
    GlucoseFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        if self.cleaned_data.get("subject_visit"):
            raise_if_not_baseline(self.cleaned_data.get("subject_visit"))
            raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        if self.cleaned_data.get("glucose_performed") == YES:
            self.validate_test_date_by_dx_date(
                "dm",
                "Diabetes",
                test_date_fld="glucose_date",
            )
            self.validate_glucose_test()


class GlucoseBaselineForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseBaselineFormValidator

    class Meta:
        model = Glucose
        fields = "__all__"
