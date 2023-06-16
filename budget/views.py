from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from budget.forms import AddIncomeForm, AddExpenseForm, CategoryForm
from budget.models import Category, BudgetEntry
from .filters import Filter
import json
from django.core.serializers.json import DjangoJSONEncoder
import io



User = get_user_model()


# Create your views here.

class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(
                request,
                template_name="registerPage.html"
            )

        return render(
            request,
            template_name="index.html"
        )


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            template_name="homePage.html"
        )


class IncomesView(LoginRequiredMixin, ListView):
    template_name = "incomes.html"
    model = BudgetEntry

    def get_queryset(self):
        return self.request.user.budgetentry_set.filter(type="income")

    def search(request):
        entries_list = request.user.budgetentry_set.filter(type="income")
        entries_filter = Filter(request.GET, queryset=entries_list)
        return render(request, 'incomes.html', {'filter': entries_filter})

    def getPdf(request):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)
        incomes = request.user.budgetentry_set.filter(type="income")

        lines = []

        for income in incomes:
            lines.append(f'{income.description} - {str(income.amount)} - {income.category.name} - {income.payment_method} - {income.date}')
            lines.append(" ")

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='incomes.pdf')


class AddIncomeView(LoginRequiredMixin, CreateView):
    model = BudgetEntry
    template_name = "form.html"
    success_url = reverse_lazy("incomes")
    form_class = AddIncomeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditIncomeView(LoginRequiredMixin, UpdateView):
    model = BudgetEntry
    template_name = "form.html"
    success_url = reverse_lazy("incomes")
    form_class = AddIncomeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['object'].user:
            return super().render_to_response(context)
        else:
            return HttpResponse('404')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteIncomeView(LoginRequiredMixin, DeleteView):
    model = BudgetEntry
    template_name = 'delete.html'
    success_url = reverse_lazy("incomes")

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['object'].user:
            return super().render_to_response(context, **response_kwargs)
        else:
            return HttpResponse('404')


class ExpensesView(LoginRequiredMixin, ListView):
    template_name = "expenses.html"
    model = BudgetEntry

    def get_queryset(self):
        return self.request.user.budgetentry_set.filter(type="expense")

    def search(request):
        entries_list = request.user.budgetentry_set.filter(type="expense")
        entries_filter = Filter(request.GET, queryset=entries_list)
        return render(request, 'expenses.html', {'filter': entries_filter})

    def getPdf(request):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)
        expenses = request.user.budgetentry_set.filter(type="expense")

        lines = []

        for expense in expenses:
            lines.append(f'{expense.description} - {str(expense.amount)} - {expense.category.name} - {expense.payment_method} - {expense.date}')
            lines.append(" ")

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='expenses.pdf')


class AddExpenseView(LoginRequiredMixin, CreateView):
    model = BudgetEntry
    template_name = "form.html"
    success_url = reverse_lazy("expenses")
    form_class = AddExpenseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditExpenseView(LoginRequiredMixin, UpdateView):
    model = BudgetEntry
    template_name = "form.html"
    success_url = reverse_lazy("expenses")
    form_class = AddExpenseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['object'].user:
            return super().render_to_response(context)
        else:
            return HttpResponse('404')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    model = BudgetEntry
    template_name = 'delete.html'
    success_url = reverse_lazy("expenses")

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['object'].user:
            return super().render_to_response(context, **response_kwargs)
        else:
            return HttpResponse('404')


class CategoriesView(LoginRequiredMixin, ListView):
    template_name = "categories.html"
    model = Category

    def get_queryset(self):
        return self.request.user.category_set.all()


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "form.html"
    success_url = reverse_lazy("categories")
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return self.request.user.category_set.all()


class EditCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "form.html"
    success_url = reverse_lazy("categories")
    form_class = CategoryForm

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['category'].user:
            return super().render_to_response(context)
        else:
            return HttpResponse('404')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'delete.html'
    success_url = reverse_lazy("categories")

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['category'].user:
            return super().render_to_response(context)
        else:
            return HttpResponse('404')


class StatisticsView(LoginRequiredMixin, ListView):
    def charts(request):
        labels = ['Incomes', 'Expenses']
        incomesSum = 0
        expensesSum = 0

        incomes = BudgetEntry.objects.filter(type="income")
        expenses = BudgetEntry.objects.filter(type="expense")
        for income in incomes:
            incomesSum = incomesSum + int(income.amount)

        for expense in expenses:
            expensesSum = expensesSum + int(expense.amount)

        return render(request, 'statistics.html', {
            'labels': labels,
            'data': [incomesSum, expensesSum],
        })

    def charts_incomes(request):
        data = []
        temp = {}

        incomes = BudgetEntry.objects.filter(type="income")

        for income in incomes:
            temp['amount'] = int(income.amount)
            temp['category'] = str(getattr(income, 'category'))
            data.append(temp)
            temp = {}

        incomes_json = json.dumps(list(data), cls=DjangoJSONEncoder)

        return render(request, 'statisticsByCategory.html', {
            'data': incomes_json,
            'title': 'incomes'
        })

    def charts_expenses(request):
        data = []
        temp = {}

        expenses = BudgetEntry.objects.filter(type="expense")

        for expense in expenses:
            temp['amount'] = int(expense.amount)
            temp['category'] = str(getattr(expense, 'category'))
            data.append(temp)
            temp = {}

        incomes_json = json.dumps(list(data), cls=DjangoJSONEncoder)

        return render(request, 'statisticsByCategory.html', {
            'data': incomes_json,
            'title': 'expenses'
        })
