import boto3 
from botocore.exceptions import ClientError
import json

from django.db import transaction
from rest_framework import status, viewsets, generics
from rest_framework.response import Response

from s3.models import Bucket
from s3.serializers import BucketCreateSerializer
from s3.const import *
from s3.exceptions import DuplicationError, ServerError


class S3ViewSet(
    viewsets.GenericViewSet,
    generics.CreateAPIView):
    """ViewSet of AWS S3 Management API."""
    queryset = Bucket.objects.all()
    serializer_class = BucketCreateSerializer

    # POST /s3
    @transaction.atomic
    def create(self, request):
        """Create Bucket, Policy, Statement models and request AWS."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        bucket = serializer.save()
        self.create_bucket(bucket)
        return Response(self.get_serializer(bucket).data, status=status.HTTP_200_OK)

    def create_bucket(self, bucket):
        """Request Bucket Create to AWS using boto3."""
        s3 = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
        try:
            bucket_name = bucket.name
            policy = {
                "Version": bucket.policy.version,
                "Statement": [{
                    "Sid": bucket.policy.statement.sid,
                    "Action": list(bucket.policy.statement.action.all().values_list('name', flat=True)),
                    "Effect": bucket.policy.statement.effect,
                    "Resource": [f"arn:aws:s3:::{bucket.name}/*", f"arn:aws:s3:::{bucket.name}"],
                    "Principal": {
                        "AWS": list(bucket.policy.statement.principal.all().values_list('arn', flat=True))
                    }
                }]
            }
            response = s3.create_bucket(
                ACL='private',
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': bucket.region
                },
            )
            s3.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy)
            ) 
            return response

        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                raise DuplicationError("Bucket name already exists.")
            else:
                return ServerError(e)

    