from django import forms
from respond_model.modelform_mixins import DrugSupplyNcdFormMixin

from mocca_lists.models import DmTreatments

from ..models import DrugSupplyDm


class DrugSupplyDmForm(DrugSupplyNcdFormMixin, forms.ModelForm):
    list_model_cls = DmTreatments
    relation_label = "drugsupplydm"

    class Meta:
        model = DrugSupplyDm
        fields = "__all__"
