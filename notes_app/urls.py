from django.urls import path

from notes_app import views


# URL Configuration for notes_app
app_name='notes_app'
urlpatterns = [
    path('', views.NotesAPIView.as_view(), name='notes_crud'),
    path('is-archive/', views.ArchiveNotesAPIView.as_view(), name='is-archive'),
    path('is-trash/', views.TrashNotesAPIView.as_view(), name='is-trah'),
    path('<id>/', views.DeleteNoteAPIView.as_view(), name='notes_delete'),
    path('labels/', views.LabelsAPIView.as_view(), name='labels_crud'),
    path('data/excel-sheet/', views.ExcelSheetAPIView.as_view(), name='excel_sheet'),
]
