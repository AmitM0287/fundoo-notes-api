from django.contrib import admin

from notes_app.models import Notes


# Register Notes model 
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'notes', 'user_id']
