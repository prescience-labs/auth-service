# Generated by Django 2.2.4 on 2019-08-23 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token_valid_timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='token valid timestamp'),
        ),
    ]
