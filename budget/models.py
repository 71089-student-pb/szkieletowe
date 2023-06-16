from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES, null=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class BudgetEntry(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('creditCard', 'Credit Card'),
        ('debitCard', 'Debit Card'),
        ('transfer', 'Bank Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.localdate().strftime('%Y-%m-%d'))
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=7, choices=ENTRY_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.amount} - {self.category}"
