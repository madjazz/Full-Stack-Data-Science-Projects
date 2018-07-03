from django.db import models
import datetime

# Create your models here.


class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    mood_field = models.TextField()
    rating = models.IntegerField(null=True)

    def __str__(self):
        return self.date.strftime("%y-%b-%d %H:%M:%S")
