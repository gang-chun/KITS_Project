from django import forms
from .models import KitInstance, Kit, Study, Location, Requisition, KitOrder


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = (
            'id', 'IRB_number', 'pet_name', 'comment', 'sponsor_name', 'requisition_form_qty', 'status',
            'start_date', 'end_date')


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ('link', 'file', 'description')


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = (
            'IRB_number', 'type_name', 'description', 'date_added', 'id', 'location')


class KitIDForm(forms.ModelForm):
        model = Kit
        fields = ('id')


class KitInstanceForm(forms.ModelForm):
    class Meta:
        model = KitInstance
        fields = (
            'id','expiration_date', 'status', 'note', 'location')
        #child_model = Kit
        #child_form_class = KitIDForm

class KitOrderForm(forms.ModelForm):
    class Meta:
        model = KitOrder
        fields = '__all__'

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class KitInstanceEditForm(forms.ModelForm):
    class Meta:
        model = KitInstance
        fields = ('status',)