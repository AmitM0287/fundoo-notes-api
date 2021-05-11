from django.contrib import admin
from notes_app.models import Notes, Labels


# Register Notes model
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'user_id']
