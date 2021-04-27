from rest_framework import serializers

from notes_app.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer
    """
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    notes = serializers.CharField(min_length=4, max_length=1200, required=True)
    class Meta:
        model = Notes
        fields = ['title', 'notes', 'user_id']


class UpdateSerializer(serializers.ModelSerializer):
    """
        Notes Serializer
    """
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    notes = serializers.CharField(min_length=4, max_length=1200, required=True)
    class Meta:
        model = Notes
        fields = ['id', 'title', 'notes']
