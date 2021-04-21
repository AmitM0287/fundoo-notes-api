from rest_framework.urlpatterns import format_suffix_patterns 
from django.urls import path, include
from . import views


# Urls to handle specific request
urlpatterns = [
    path('login/', views.UserLogin.as_view()),
    path('register/', views.UserRegister.as_view()),
    path('update/<int:id>/', views.UserUpdate.as_view()),
    path('reset/password/<int:id>/', views.ResetPassword.as_view()),
    path('delete/<int:id>/', views.UserDelete.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
