# Generated by Django 5.1.3 on 2024-12-01 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_account_options_account_avatar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_following', to=settings.AUTH_USER_MODEL, verbose_name='кто подписался')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_followers', to=settings.AUTH_USER_MODEL, verbose_name='на кого подписался')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'unique_together': {('following', 'follower')},
            },
        ),
    ]