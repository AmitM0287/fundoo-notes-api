from django.urls import path

from notes_app import views


# URL Configuration for note_app
app_name='notes_app'
urlpatterns = [
    path('', views.NotesCRUD.as_view(), name='notes_crud'),
    path('labels/', views.LabelsCRUD.as_view(), name='labels_crud'),
]
