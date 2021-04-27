from rest_framework import serializers

from notes_app.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer
    """
    class Meta:
        model = Notes
        fields = ['title', 'notes', 'user_id']


class NotesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'notes']
