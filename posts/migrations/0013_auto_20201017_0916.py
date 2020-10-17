# Generated by Django 2.2.6 on 2020-10-17 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0012_auto_20200831_0917'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'author')},
        ),
        migrations.CreateModel(
            name='SubGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('group', models.ForeignKey(blank=True, help_text='Выберите Категорию, если хотите 😉', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subgroup', to='posts.Group', verbose_name='Категории')),
            ],
        ),
    ]