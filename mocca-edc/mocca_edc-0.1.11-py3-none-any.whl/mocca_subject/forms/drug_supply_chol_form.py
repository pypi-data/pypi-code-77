from django import forms
from respond_model.modelform_mixins import DrugSupplyNcdFormMixin

from mocca_lists.models import DmTreatments

from ..models import DrugSupplyChol


class DrugSupplyCholForm(DrugSupplyNcdFormMixin, forms.ModelForm):
    list_model_cls = DmTreatments
    relation_label = "drugsupplychol"

    class Meta:
        model = DrugSupplyChol
        fields = "__all__"
