# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.BooleanField(default=b'male', choices=[(1, b'male'), (2, b'female')])),
                ('location', models.CharField(default=b'Empty', max_length=100)),
                ('favorite_animal', models.CharField(default=b'Dragons', max_length=20)),
                ('job', models.CharField(default=b'Empty', max_length=50)),
                ('education', models.CharField(default=b'Empty', max_length=50)),
                ('short_description', models.TextField(default=b'Empty')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
