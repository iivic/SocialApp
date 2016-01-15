# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_details', '0009_auto_20151123_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='friend',
            new_name='friends',
        ),
    ]
