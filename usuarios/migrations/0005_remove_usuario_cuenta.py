# Generated by Django 5.1.3 on 2024-11-23 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuario_cuenta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='cuenta',
        ),
    ]