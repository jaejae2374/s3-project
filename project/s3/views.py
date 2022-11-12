from django.db import transaction
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from s3.serializers import BucketCreateSerializer
from s3.models import Bucket
import boto3
from botocore.exceptions import ClientError
import json
__aws_access_key_id__ = "AKIAYNIYTU7NX3W6FPWE"
__aws_secret_access_key__ = "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"


class S3ViewSet(
    viewsets.GenericViewSet,
    generics.CreateAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketCreateSerializer

    # POST /s3
    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        bucket = serializer.save()
        try:
            self.create_bucket(bucket)
        except Exception as e:
            print(e)
            return Response("wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(self.get_serializer(bucket).data, status=status.HTTP_200_OK)

    def create_bucket(self, bucket):
        s3 = boto3.client(
            's3',
            aws_access_key_id = __aws_access_key_id__,
            aws_secret_access_key=__aws_secret_access_key__
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
            print(json.dumps(policy))
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
                raise Exception("already exists.")
            else:
                raise Exception(e)

    