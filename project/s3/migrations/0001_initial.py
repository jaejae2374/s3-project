# Generated by Django 4.1.2 on 2022-11-12 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arn', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=20)),
                ('bucket', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='s3.bucket')),
            ],
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sid', models.CharField(max_length=50)),
                ('effect', models.CharField(choices=[('allow', 'allow'), ('deny', 'deny')], max_length=10)),
                ('action', models.ManyToManyField(null=True, to='s3.action')),
                ('policy', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='s3.policy')),
                ('principal', models.ManyToManyField(null=True, to='s3.client')),
                ('resource', models.ManyToManyField(null=True, to='s3.bucket')),
            ],
        ),
    ]