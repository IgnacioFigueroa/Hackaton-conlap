from django.db import models

class Message(models.Model):
    update_id = models.IntegerField()
    message_id = models.IntegerField()
    user_id = models.IntegerField()
    user_name = models.TextField()
    user_last = models.TextField()
    languaje_code = models.TextField()
    chat_id = models.IntegerField()
    chat_title = models.IntegerField()
    type = models.TextField()
    date = models.IntegerField()
    text = models.TextField()
# Create your models here.
