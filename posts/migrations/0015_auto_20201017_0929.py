# Generated by Django 2.2.6 on 2020-10-17 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_subgroup_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subgroup',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]