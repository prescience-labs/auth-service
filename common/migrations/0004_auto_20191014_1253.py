# Generated by Django 2.2.4 on 2019-10-14 12:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('common', '0003_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='permissions',
            field=models.ManyToManyField(to='auth.Permission'),
        ),
        migrations.AlterField(
            model_name='client',
            name='secret',
            field=models.CharField(default=uuid.UUID('247de8da-67c6-48f5-8905-9d77d41120fa'), max_length=255, unique=True, verbose_name='client token'),
        ),
        migrations.AlterField(
            model_name='client',
            name='token',
            field=models.CharField(default=uuid.UUID('2651fcb9-e8f0-4547-821b-e5ef4dde5b3f'), max_length=255, unique=True, verbose_name='client token'),
        ),
    ]