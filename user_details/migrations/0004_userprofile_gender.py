# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_details', '0003_remove_userprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'male', max_length=5, choices=[(b'1', b'male'), (b'2', b'female')]),
        ),
    ]
