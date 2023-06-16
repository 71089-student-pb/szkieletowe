from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('changePassword', PasswordChangeView.as_view(), name='changePassword'),
]
