from django.db import transaction
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from s3.serializers import BucketCreateSerializer
from s3.models import Bucket


class S3ViewSet(
    viewsets.GenericViewSet,
    generics.CreateAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketCreateSerializer

    # POST /s3
    @transaction.atomic
    def create(self, request):
        pass


    