# Generated by Django 5.1.7 on 2025-04-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_shared_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
