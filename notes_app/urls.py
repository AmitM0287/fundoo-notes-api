from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path

from . import views


# Urls to handle specific request
urlpatterns = [
    path('create/', views.CreateNotes.as_view()),
    path('update/<int:id>/', views.UpdateNotes.as_view()),
    path('delete/<int:id>/', views.DeleteNotes.as_view()),
    path('list/<int:id>/', views.ListNotes.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
