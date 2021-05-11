import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db


class TestNotesModel:
    """
        TestNotesModel : notes_app.Notes
    """
    def test_init(self):
        notes_obj = mixer.blend('notes_app.Notes')
        assert notes_obj.id == 1, 'should save an instance'


class TestLabelsModel:
    """
        TestLabelsModel : notes_app.Labels
    """
    def test_init(self):
        labels_obj = mixer.blend('notes_app.Labels')
        assert labels_obj.id == 1, 'should save an instance'
