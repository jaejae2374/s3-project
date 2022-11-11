from s3.models import *
from rest_framework import serializers
from s3.const import *
from s3.exceptions import FieldError

class BucketCreateSerializer(serializers.ModelSerializer):
    policy = serializers.SerializerMethodField()

    class Meta:
        model = Bucket
        fields = (
            'id',
            'name',
            'region',
            'policy'
        )

    def create(self, validated_data):
        bucket = Bucket.objects.create(
            name = validated_data['bucket_name'],
            region = validated_data.get('region', 'us-east-2')
        )
        policy = Policy.objects.create(
            version = POLICY_VER,
            bucket = bucket
        )
        statement = Statement.objects.create(
            sid=f"{validated_data['bucket_name']}-stmt",
            policy = policy,
            effect = DENY,
            action = Action.objects.get_or_create(
                name = GET_OBJECT
            )
        )
        statement.resource.add(bucket)
        statement.action.add(
            Action.objects.get_or_create(
                name = GET_OBJECT
        ))
        statement.principal.add(
            Client.objects.get_or_create(
                name = AUTHORIZED_ARN
        ))
        return bucket

    def validate(self, data):
        if not data.get('bucket_name'):
            raise FieldError("bucket_name required.")
        return data
    
    def get_policy(self, instance):
        return PolicySerializer(instance.policy).data


class PolicySerializer(serializers.ModelSerializer):
    statement = serializers.SerializerMethodField()

    class Meta:
        model = Bucket
        fields = (
            'version',
            'statement'
        )
    
    def get_statement(self, instance):
        return StatementSerializer(instance.statement).data

class StatementSerializer(serializers.ModelSerializer):
    resource = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    principal = serializers.SerializerMethodField()

    class Meta:
        model = Bucket
        fields = (
            'sid',
            'effect',
            'resource',
            'action',
            'principal'
        )

    def get_resource(self, instance):
        return list(map(lambda x: f"arn:aws:s3:::{x.name}", instance.resource.all()))
    
    def get_action(self, instance):
        return instance.action.all().values_list('name', flat=True)

    def get_principal(self, instance):
        return instance.principal.all().values_list('arn', flat=True)