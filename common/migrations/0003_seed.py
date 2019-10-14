from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

def insert_can_force_user_login_permission(apps, schema_editor):
    Client  = apps.get_model('common', 'Client')
    ct      = ContentType.objects.get_for_model(Client)
    return Permission.objects.create(
        codename='can_force_user_login',
        name='Can force user login',
        content_type=ct,
    )

class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('common', '0002_client'),
    ]

    operations = [
        migrations.RunPython(insert_can_force_user_login_permission),
    ]
