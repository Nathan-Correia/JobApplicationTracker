# Generated by Django 5.1.5 on 2025-01-18 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_resume_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='user',
            field=models.CharField(blank=True, default='1', max_length=255, null=True),
        ),
    ]
