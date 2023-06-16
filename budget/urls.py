from django.urls import path
from budget.models import BudgetEntry
from budget import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home', views.HomeView.as_view(), name="home"),
    path('incomes', views.IncomesView.search, name="incomes"),
    path('getIncomes', views.IncomesView.getPdf, name="getIncomes"),
    path('addIncome', views.AddIncomeView.as_view(), name="addIncome"),
    path('editIncome/<pk>/', views.EditIncomeView.as_view(), name="editIncome"),
    path('deleteIncome/<pk>/', views.DeleteIncomeView.as_view(), name="deleteIncome"),
    path('expenses', views.ExpensesView.search, name="expenses"),
    path('getExpenses', views.ExpensesView.getPdf, name="getExpenses"),
    path('addExpense', views.AddExpenseView.as_view(), name="addExpense"),
    path('editExpense/<pk>/', views.EditExpenseView.as_view(), name="editExpense"),
    path('deleteExpense/<pk>/', views.DeleteExpenseView.as_view(), name="deleteExpense"),
    path('categories/', views.CategoriesView.as_view(), name="categories"),
    path('addCategory/', views.AddCategoryView.as_view(), name="addCategory"),
    path('editCategory/<pk>/', views.EditCategoryView.as_view(), name="editCategory"),
    path('deleteCatefory/<pk>/', views.DeleteCategoryView.as_view(), name="deleteCategory"),
    path('statistics', views.StatisticsView.charts, name="statistics"),
    path('statisticsIncomes', views.StatisticsView.charts_incomes, name="statisticsIncomes"),
    path('statisticsExpenses', views.StatisticsView.charts_expenses, name="statisticsExpenses"),
]
