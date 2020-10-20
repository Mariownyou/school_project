# Generated by Django 2.2.6 on 2020-10-20 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_remove_post_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='group',
            field=models.ForeignKey(help_text='Выберите Категорию, если хотите 😉', on_delete=django.db.models.deletion.CASCADE, related_name='category', to='posts.Group', verbose_name='Категории'),
        ),
    ]