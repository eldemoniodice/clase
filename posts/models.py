# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Client(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    usertype=models.CharField(max_length=200)

class Project(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    projectname=models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    value=models.DecimalField(max_digits=12, decimal_places=2)


class Message(models.Model):
    sender=models.ForeignKey(User, related_name='%(class)s_sender', on_delete=models.CASCADE)
    recipient=models.ForeignKey(User, related_name='%(class)s_recipient', on_delete=models.CASCADE)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    message=models.CharField(max_length=2000)

    def __unicode__(self):
        return unicode(self.user)
