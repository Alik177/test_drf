from django_filters.rest_framework import FilterSet, NumberFilter
from .models import *

class BookFilter(FilterSet):
    price_maximum = NumberFilter(field_name='price', lookup_expr='lte')
    # При получении параметра price_maximum будет брать lte(less than or equal) от этого значения
    price_minimum = NumberFilter(field_name='price', lookup_expr='gte')
    # При получении параметра price_minimum будет брать gte(greater than or equal) от этого значения

    class Meta:
        model = Book
        fields = ['price']