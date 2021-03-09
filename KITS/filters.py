import django_filters
from .models import *


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
            'type_name', 'date_added', "IRB_number_id",
        )
