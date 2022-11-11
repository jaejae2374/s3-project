from django.urls import include, path
from rest_framework.routers import SimpleRouter
from s3.views import S3ViewSet

app_name = 's3'

router = SimpleRouter() 
router.register('s3', S3ViewSet, basename='s3')

urlpatterns = [
    path('', include((router.urls))),
]