from django.contrib.auth.models import User
from django.db import models


class Labels(models.Model):
    """
     Labels Model
    """
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Notes(models.Model):
    """
        Notes Model
    """
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=1200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels)
