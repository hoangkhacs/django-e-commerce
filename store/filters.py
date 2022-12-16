import django_filters

from store.models import Product


class ProductFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(
        field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(
        field_name='price', lookup_expr='lt')
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = {'public_company', 'author', 'price'}
