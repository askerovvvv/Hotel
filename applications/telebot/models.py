from django.db import models


class TeleSettings(models.Model):
    token = models.CharField(max_length=200)
    chat = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.chat
