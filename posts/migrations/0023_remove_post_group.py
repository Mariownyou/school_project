# Generated by Django 2.2.6 on 2020-10-17 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20201017_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='group',
        ),
    ]
