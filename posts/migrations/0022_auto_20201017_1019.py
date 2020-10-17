# Generated by Django 2.2.6 on 2020-10-17 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_auto_20201017_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Выберите категорию, если хотите 😉', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.Category', verbose_name='Категория'),
        ),
    ]