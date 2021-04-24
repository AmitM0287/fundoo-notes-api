from django.contrib.auth.models import User
from django.db import models


# Notes model
class Notes(models.Model):
    title = models.CharField(max_length=400)
    notes = models.CharField(max_length=1200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
