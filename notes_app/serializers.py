from rest_framework import serializers

from notes_app.models import Notes


# Notes Serializer
class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'notes', 'user_id']


# Notes Update Serializer
class NotesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'notes']
