# Generated by Django 2.2.4 on 2019-10-15 13:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20191014_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.CharField(default=uuid.UUID('2038319a-4db7-4697-b40a-d9678d5f9ac1'), help_text='We use a different ID than the object ID to preserve database security', max_length=255, unique=True, verbose_name='client ID'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.CharField(default=uuid.UUID('1fb5ac9b-88b6-4032-b240-5c4b99ed9df5'), max_length=255, unique=True, verbose_name='client secret'),
        ),
    ]