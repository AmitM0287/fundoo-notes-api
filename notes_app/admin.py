from django.contrib import admin
from .models import Notes


# Register Notes model 
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['title', 'notes', 'user_id']
