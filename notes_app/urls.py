from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path

from . import views


# Urls to handle specific request
urlpatterns = [
    path('notes/', views.NotesList.as_view()),
    path('notes/<int:pk>/', views.NotesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
