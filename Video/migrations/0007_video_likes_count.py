# Generated by Django 4.1.3 on 2023-01-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Video', '0006_alter_video_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='likes_count',
            field=models.BigIntegerField(default=0, verbose_name='تعداد لایک ها'),
        ),
    ]