# Generated by Django 5.1.3 on 2024-12-05 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='my_following',
            field=models.ManyToManyField(related_name='my_followers', to='posts.userprofile'),
        ),
    ]
