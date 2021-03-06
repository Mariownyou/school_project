# Generated by Django 2.2.6 on 2020-10-17 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_subgroup_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('title', models.CharField(help_text='Назовите категорию', max_length=200, unique=True)),
                ('group', models.ForeignKey(blank=True, help_text='Выберите Категорию, если хотите 😉', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='posts.Group', verbose_name='Категории')),
            ],
        ),
        migrations.DeleteModel(
            name='SubGroup',
        ),
    ]
