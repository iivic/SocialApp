# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_details', '0007_userprofile_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='friends',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friend',
            field=models.ForeignKey(related_name='UserFriend', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
