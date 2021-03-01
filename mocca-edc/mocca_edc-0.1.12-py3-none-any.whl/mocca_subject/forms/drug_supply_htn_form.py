from django import forms
from respond_model.modelform_mixins import DrugSupplyNcdFormMixin

from mocca_lists.models import HtnTreatments

from ..models import DrugSupplyHtn


class DrugSupplyHtnForm(DrugSupplyNcdFormMixin, forms.ModelForm):
    list_model_cls = HtnTreatments
    relation_label = "drugsupplyhtn"

    class Meta:
        model = DrugSupplyHtn
        fields = "__all__"
