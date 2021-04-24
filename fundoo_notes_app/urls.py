from django.urls import path, include

from django.contrib import admin


# URL Configuration for fundoo_notes_app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls', namespace='auth_app')),
    path('notes/', include('notes_app.urls', namespace='notes_app')),
]
