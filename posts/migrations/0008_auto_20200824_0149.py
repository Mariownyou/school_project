# Generated by Django 2.2.9 on 2020-08-23 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Картинка украсит ваш пост', null=True, upload_to='media/', verbose_name='Картинка'),
        ),
    ]
