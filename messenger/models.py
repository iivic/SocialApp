from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    subject = models.CharField(max_length=255)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.subject


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(User)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'
