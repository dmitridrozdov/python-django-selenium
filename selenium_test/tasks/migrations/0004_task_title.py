# Generated by Django 3.0.7 on 2020-06-09 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200609_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default='runtest', max_length=200),
        ),
    ]
