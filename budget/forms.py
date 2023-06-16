from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django import forms
import django_filters

from budget.models import Category, BudgetEntry


class AddExpenseForm(LoginRequiredMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = self.request.user.category_set.filter(category="expense")
        self.fields['payment_method'].queryset = BudgetEntry.payment_method

    description = forms.CharField(max_length=255, required=False)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=128, required=True)
    date = forms.DateField
    type = forms.CharField(max_length=7, required=True, initial='expense', disabled=True)

    class Meta:
        model = BudgetEntry
        fields = ("amount", "description", "category", "payment_method", "date", "type")


class AddIncomeForm(LoginRequiredMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = self.request.user.category_set.filter(category="income")
        self.fields['payment_method'].queryset = BudgetEntry.payment_method

    description = forms.CharField(max_length=255, required=False)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=128, required=True)
    date = forms.DateField
    type = forms.CharField(max_length=7, required=True, initial='income', disabled=True)

    class Meta:
        model = BudgetEntry
        fields = ["amount", "description", "category", "payment_method", "date", "type"]


class CategoryForm(LoginRequiredMixin, forms.ModelForm):
    name = forms.CharField(max_length=128, required=False)
    category = forms.ChoiceField
    description = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Category
        fields = ["name", "category", "description"]
