from django.urls import path, include

from auth_app import views


# URL Configuration for auth_app
app_name='auth_app'
urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='user_login'),
    path('register/', views.RegisterAPIView.as_view(), name='user_register'),
    path('reset/username/', views.ResetUsernameAPIView.as_view(), name='user_reset_username'),
    path('reset/password/', views.ResetPasswordAPIView.as_view(), name='user_reset_password'),
    path('delete/', views.UserDeleteAPIView.as_view(), name='user_delete'),
    path('activate/<token>/', views.VerifyEmail.as_view(), name='activate_user'),
]
