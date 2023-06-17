from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class groupdatainfo(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    userg = models.CharField(max_length=100)
    groupname = models.CharField(max_length=100)


class appliancesdatainfo(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    usera = models.CharField(max_length=100)
    gpname = models.CharField(max_length=100)
    appliancename = models.CharField(max_length=100)
    status = models.CharField(max_length=10)





    