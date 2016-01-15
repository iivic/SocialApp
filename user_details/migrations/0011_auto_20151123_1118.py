# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_details', '0010_auto_20151123_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(related_name='UserFriend', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
