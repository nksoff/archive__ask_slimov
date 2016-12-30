# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ask_slimov', '0002_auto_20151115_1032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
