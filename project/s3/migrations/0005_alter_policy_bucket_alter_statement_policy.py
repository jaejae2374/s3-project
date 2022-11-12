# Generated by Django 4.1.2 on 2022-11-12 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('s3', '0004_alter_statement_action_alter_statement_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='bucket',
            field=models.OneToOneField(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='s3.bucket'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='policy',
            field=models.OneToOneField(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='s3.policy'),
        ),
    ]
