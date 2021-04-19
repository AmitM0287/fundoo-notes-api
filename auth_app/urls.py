from django.urls import path, include
from . import views


# Urls to handle specific request
urlpatterns = [
    path('user/login/', views.UserLogin.as_view()),
    path('user/register/', views.UserRegistration.as_view()),
]
