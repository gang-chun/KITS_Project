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
        fields = '__all__'


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = (
            'IRB_number', 'type_name', 'description', 'date_added', 'id', 'location')


class KitIDForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ('id', )


class KitInstanceForm(forms.ModelForm):
    class Meta:
        model = KitInstance
        fields = (
            'id', 'expiration_date', 'status', 'note', 'location')
        # child_model = Kit
        # child_form_class = KitIDForm


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
        child_model = Kit
        fields = ('status',)
        child_field = ('id')
# id = forms.ModelChoiceField(queryset=Kit.objects.values('id'), to_field_name='id',empty_label="Select Kit")
        # id= forms.ModelChoiceField(queryset=Kit.objects.values('id'))
        #fields = forms.ModelChoiceField(queryset=KitInstance.objects.all(),
#                                       limit_choices_to='status', widget=forms.Select(attrs={'onchange': 'submit();'}))

class KitInstanceKitIDEditForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ('id',)