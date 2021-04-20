from rest_framework import serializers
from .models import Notes


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer
    """
    class Meta:
        model = Notes
        fields = ['id', 'title', 'notes', 'user_id']
