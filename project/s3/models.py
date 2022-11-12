"""Models for AWS S3 Management API."""

from django.db import models
from s3.const import *

class Bucket(models.Model):
    """
    S3 Bucket Model.

        # Fields
        name (str): name of bucket.
        region (str): region of bucket.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=20, blank=True)

class Policy(models.Model):
    """
    S3 Bucket Policy Model.

        # Fields
        version (str): version of policy. Static value (2012-10-17).
        bucket (Bucket): One to One relation with Bucket.
    """
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20)
    bucket = models.OneToOneField(Bucket, on_delete=models.CASCADE, null=True, db_constraint=False)

class Action(models.Model):
    """
    Action Model in S3 Bucket Policy's Statement. (Static)

        # Fields
        name (str): Action's name. (ex. s3:ListBucket)
    """
    name = models.CharField(max_length=30)

class Client(models.Model):
    """
    Client Model in S3 Bucket Policy's Statement.

        # Fields
        arn (str): User / Roles's Arn.
    """
    arn = models.CharField(max_length=1000)

class Statement(models.Model):
    """
    Statement Model in S3 Bucket Policy.

        # Fields
        sid (str): name of statement.
        policy (Policy): One to One relation with Policy.
        effect (str): Related to Permission. (Allow, Deny)
        action (Action): Many to Many relations with Action.
        principal (Client): Subject of actions. Many to Many relations with Client.
    """
    id = models.AutoField(primary_key=True)
    sid = models.CharField(max_length=50)
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, null=True, db_constraint=False)
    effect = models.CharField(max_length=10, choices=((ALLOW, "Allow"), (DENY, "Deny")))
    action = models.ManyToManyField(Action, db_constraint=False)
    principal = models.ManyToManyField(Client, db_constraint=False)
