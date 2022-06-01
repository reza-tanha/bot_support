from django.db import models

class UserBot(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=70)
    lastname = models.CharField(max_length=70)
    username = models.CharField(max_length=70)
    isblock = models.BooleanField(default=False)
    step = models.CharField(max_length=70)
    tab = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    user = models.ForeignKey(UserBot, on_delete=models.CASCADE)
    message_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


