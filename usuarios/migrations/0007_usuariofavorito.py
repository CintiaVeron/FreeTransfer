# Generated by Django 5.1.3 on 2024-11-25 02:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_transferencia_motivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioFavorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_favorito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='es_favorito_de', to=settings.AUTH_USER_MODEL)),
                ('usuario_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos_origen', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('usuario_origen', 'usuario_favorito'), name='unique_favorito')],
            },
        ),
    ]
