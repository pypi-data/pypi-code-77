from django import forms
from edc_constants.constants import YES
from edc_form_validators import FormValidator
from edc_model.models import estimated_date_from_ago


class GlucoseFormValidatorMixin(FormValidator):
    def validate_glucose_test(self):
        if self.cleaned_data.get("glucose_date") and self.cleaned_data.get("dx_ago"):
            if (
                estimated_date_from_ago(data=self.cleaned_data, ago_field="dx_ago")
                - self.cleaned_data.get("glucose_date")
            ).days > 1:
                raise forms.ValidationError(
                    {"glucose_date": "Invalid. Cannot be before diagnosis."}
                )
        self.required_if(YES, field="glucose_performed", field_required="glucose_fasted")
        self.required_if(YES, field="glucose_performed", field_required="glucose_date")
        self.required_if(YES, field="glucose_performed", field_required="glucose")
        self.required_if(YES, field="glucose_performed", field_required="glucose_quantifier")
        self.applicable_if(YES, field="glucose_performed", field_applicable="glucose_units")
