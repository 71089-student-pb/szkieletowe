import django_filters
from budget.models import BudgetEntry
from django.contrib.auth.models import User


class Filter(django_filters.FilterSet):
    amount = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains', field_name='category__name')
    payment_method = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateTimeFilter(lookup_expr='icontains')

    class Meta:
        model = BudgetEntry
        fields = ['amount', 'description', 'category', 'payment_method', 'date']
