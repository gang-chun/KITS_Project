import django_filters
from .models import *
from django.db.models import F


class StudyFilter(django_filters.FilterSet):
    class Meta:
        model = Study
        fields = (
            'IRB_number', 'pet_name', 'status',
        )


class KitFilter(django_filters.FilterSet):
    class Meta:
        model = Kit
        fields = (
            "IRB_number_id", 'type_name'
        )

