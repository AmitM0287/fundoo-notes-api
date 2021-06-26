from rest_framework import serializers

from notes_app.models import Notes, Labels


class NotesSerializer(serializers.ModelSerializer):
    """
        Notes Serializer : title, description
    """
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'isArchive', 'isTrash']


class LabelsSerializer(serializers.ModelSerializer):
    """
        Labels Serializer : name
    """
    name = serializers.CharField(min_length=2, max_length=200, required=True)
    
    class Meta:
        model = Labels
        fields = ['name']
