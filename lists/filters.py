from django_filters import rest_framework as filters
from lists.models import List, ListTypes

class ListFilter(filters.FilterSet):
    list_type = filters.ChoiceFilter(choices=ListTypes.choices)

    class Meta:
        model = List
        fields = ['list_type', 'organization_uuid']