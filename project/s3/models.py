from django.db import models
from s3.const import *

class Bucket(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=20)

class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20)
    bucket = models.OneToOneField(Bucket, on_delete=models.CASCADE, null=True)

class Action(models.Model):
    name = models.CharField(max_length=30)

class Client(models.Model):
    arn = models.CharField(max_length=1000)

class Statement(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.CharField(max_length=50)
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, null=True)
    effect = models.CharField(max_length=10, choices=((ALLOW, "allow"), (DENY, "deny")))
    resource = models.ManyToManyField(Bucket, on_delete=models.PROTECT, null=True)
    action = models.ManyToManyField(Action, on_delete=models.PROTECT, null=True)
    principal = models.ManyToManyField(Client, on_delete=models.PROTECT, null=True)



