from django.http import JsonResponse
from logging_configuration.logging_config import get_logger
from django.views import View
from .models import Notes
from django.contrib.auth.models import User


# Get logger to put exceptions into exceptions.log file
logger = get_logger()


"""
    SaveNotes
"""
class SaveNotes(View):
    def post(self, request, *args, **kwargs):
        try:
            # Taking user inputs
            title = request.POST['title']
            notes = request.POST['notes']
            user_id = request.POST['user_id']
            user = User.objects.get(id=user_id)
            # Save notes
            notes = Notes(title=title, notes=notes, user_id=user)
            notes.save()
            return JsonResponse({'Status': 200, 'Message': 'Notes saved successfully!'})
        except Exception as e:
            logger.exception(e)
            return JsonResponse({'Status': 'NA', 'Message': 'Oops! Something went wrong. Please try again...'})
