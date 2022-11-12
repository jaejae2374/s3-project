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
            name = validated_data['name'],
            region = validated_data['region']
        )
        policy = Policy.objects.create(
            version = POLICY_VER,
            bucket = bucket
        )
        statement = Statement.objects.create(
            sid=f"{validated_data['name']}-stmt",
            policy = policy,
            effect = DENY
        )
        get_obj, _ = Action.objects.get_or_create(name = GET_OBJECT)
        list_bck, _ = Action.objects.get_or_create(name = LIST_BUCKET)
        print(get_obj.name, list_bck.name)
        statement.action.set(
            [get_obj, list_bck]
        )
        statement.principal.set(
            Client.objects.get_or_create(
                arn = AUTHORIZED_ARN
        ))
        return bucket

    def validate(self, data):
        if not data.get('name'):
            raise FieldError("bucket_name required.")
        if not data.get('region'):
            data['region'] = 'us-east-2'
        return data
    
    def get_policy(self, instance):
        return PolicySerializer(instance.policy).data


class PolicySerializer(serializers.ModelSerializer):
    statement = serializers.SerializerMethodField()

    class Meta:
        model = Policy
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
        model = Statement
        fields = (
            'sid',
            'effect',
            'resource',
            'action',
            'principal'
        )

    def get_resource(self, instance):
        return [f"arn:aws:s3:::{instance.policy.bucket.name}"]
    
    def get_action(self, instance):
        return instance.action.all().values_list('name', flat=True)

    def get_principal(self, instance):
        return instance.principal.all().values_list('arn', flat=True)