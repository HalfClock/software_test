from django.db import models

# Create your models here.
from django.db.models import CASCADE


class List(models.Model):
    pass

class Item(models.Model):

    text = models.TextField(default='')
    list = models.ForeignKey(List,CASCADE,default=None)

