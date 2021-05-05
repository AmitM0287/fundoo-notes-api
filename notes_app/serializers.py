from rest_framework import serializers

from notes_app.models import Notes, Labels


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer
    """
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    notes = serializers.CharField(min_length=4, max_length=1200, required=True)
    class Meta:
        model = Notes
        fields = ['title', 'notes']


class LabelsSerializer(serializers.ModelSerializer):
    """
        Labels Serializer
    """
    class Meta:
        model = Labels
        fields = ['name']
