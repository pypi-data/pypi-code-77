from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_model.form_validators import (
    CrfFormValidatorMixin,
    DrugRefillFormValidatorMixin,
)

from ..models import DrugRefillHtn


class DrugRefillHtnFormValidator(
    DrugRefillFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    pass


class DrugRefillHtnForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillHtnFormValidator

    class Meta:
        model = DrugRefillHtn
        fields = "__all__"
