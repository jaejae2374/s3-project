# Generated by Django 4.1.2 on 2022-11-12 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3', '0006_alter_statement_action_alter_statement_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='effect',
            field=models.CharField(choices=[('allow', 'Allow'), ('deny', 'Deny')], max_length=10),
        ),
    ]
