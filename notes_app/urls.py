from django.urls import path
from . import views


# Urls to handle specific request
urlpatterns = [
    path('user/notes/save/', views.SaveNotes.as_view()),
]
