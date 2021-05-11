from django.urls import path

from notes_app import views


# URL Configuration for notes_app
app_name='notes_app'
urlpatterns = [
    path('', views.NotesAPIView.as_view(), name='notes_crud'),
    path('labels/', views.LabelsAPIView.as_view(), name='labels_crud'),
]
