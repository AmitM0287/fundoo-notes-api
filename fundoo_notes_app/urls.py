from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# schema_view
schema_view = get_schema_view(
   openapi.Info(
      title="Fundoo Notes API",
      default_version='AM',
      description="Fundoo notes api helps to create, update, delete notes.",
      # terms_of_service="https://terms/services",
      contact=openapi.Contact(email="amitmanna0287@gmail.com"),
      # license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# URL Configuration for fundoo_notes_app
urlpatterns = [
    path('', TemplateView.as_view(template_name='social_app/index.html')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('user/', include('auth_app.urls', namespace='auth_app')),
    path('user/notes/', include('notes_app.urls', namespace='notes_app')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
