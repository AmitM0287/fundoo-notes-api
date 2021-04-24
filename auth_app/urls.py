from django.urls import path, include

from . import views


# URL Configuration for auth_app
app_name='auth_app'
urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='auth_login'),
    path('register/', views.UserRegister.as_view(), name='auth_register'),
    path('reset/password/', views.ResetPassword.as_view(), name='auth_reset_pass'),
]
