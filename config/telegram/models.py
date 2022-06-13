from django.db import models

class UserBot(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=70, null=True, blank=True)
    lastname = models.CharField(max_length=70, null=True, blank=True)
    username = models.CharField(max_length=70, null=True, blank=True)
    isblock = models.BooleanField(default=False)
    step = models.CharField(max_length=70, null=True, blank=True)
    tab = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SponserChannel(models.Model):
    username = models.CharField(max_length=120, unique=True, verbose_name='Channel Username')
    def __str__(self):
        return self.username
    


class Message(models.Model):
    user = models.ForeignKey(UserBot, on_delete=models.CASCADE)
    message_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


