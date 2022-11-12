from django.db import models
from s3.const import *

class Bucket(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=20, blank=True)

class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20)
    bucket = models.OneToOneField(Bucket, on_delete=models.CASCADE, null=True, db_constraint=False)

class Action(models.Model):
    name = models.CharField(max_length=30)

class Client(models.Model):
    arn = models.CharField(max_length=1000)

class Statement(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.CharField(max_length=50)
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, null=True, db_constraint=False)
    effect = models.CharField(max_length=10, choices=((ALLOW, "Allow"), (DENY, "Deny")))
    action = models.ManyToManyField(Action, db_constraint=False)
    principal = models.ManyToManyField(Client, db_constraint=False)



