# Generated by Django 5.0.4 on 2024-05-02 13:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-publish_at']},
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='blog_post_publish_bb7600_idx',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='publish',
            new_name='publish_at',
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish_at'], name='blog_post_publish_bc5a66_idx'),
        ),
    ]
