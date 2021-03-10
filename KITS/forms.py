from django import forms
from .models import KitOrder, KitInstance, Kit, Study, Location


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = (
            'id', 'kit_order', 'IRB_number', 'pet_name', 'comment', 'sponsor_name', 'requisition_form_qty', 'status',
            'start_date', 'end_date')


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = (
            'id', 'type_name', 'description', 'IRB_number', 'date_added')


class KitIDForm(forms.ModelForm):
        model = Kit
        fields = ('id')


class KitInstanceForm(forms.ModelForm):
    class Meta:
        model = KitInstance
        fields = (
            'id', 'expiration_date', 'status', 'note')
        child_model = KitInstance
        child_form_class = KitIDForm
