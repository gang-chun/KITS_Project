import django_filters
from .models import *

class StudyFilter(django_filters.FilterSet):
    class Meta:
        model = Study
        fields = (
            'IRB_number', 'status',
        )
