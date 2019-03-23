from django.db import models

class Message(models.Model):
    update_id = models.IntegerField()
    message_id = models.IntegerField()
    user_id = models.IntegerField()
    user_name = models.CharField()
    user_last = models.CharField()
    languaje_code = models.CharField()
    chat_id = models.IntegerField()
    chat_title = models.IntegerField()
    type = models.CharField()
    date = models.IntegerField()
    text = models.CharField()
# Create your models here.
