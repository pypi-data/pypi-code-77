from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from mocca_form_validators.form_validators import BloodResultsFormValidatorMixin
from mocca_labs import fbc_panel

from ...models import BloodResultsFbc


class BloodResultsFbcFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "fbc_requisition"
    assay_datetime_field = "fbc_assay_datetime"
    field_names = ["haemoglobin", "hct", "rbc", "wbc", "platelets"]
    panels = [fbc_panel]


class BloodResultsFbcForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsFbcFormValidator

    class Meta:
        model = BloodResultsFbc
        fields = "__all__"
