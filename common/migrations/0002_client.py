# Generated by Django 2.2.4 on 2019-10-14 12:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('token', models.CharField(default=uuid.UUID('c2b3f047-dda0-4435-8a47-0051b9273c77'), max_length=255, unique=True, verbose_name='client token')),
                ('secret', models.CharField(default=uuid.UUID('2fcbb051-330b-4391-a870-b803c62db4a9'), max_length=255, unique=True, verbose_name='client token')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
