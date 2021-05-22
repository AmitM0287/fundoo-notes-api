from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView


# URL Configuration for fundoo_notes_app
urlpatterns = [
    path('', TemplateView.as_view(template_name='social_app/index.html')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('user/', include('auth_app.urls', namespace='auth_app')),
    path('user/notes/', include('notes_app.urls', namespace='notes_app')),
]
