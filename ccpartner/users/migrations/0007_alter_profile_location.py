# Generated by Django 3.2.4 on 2022-01-07 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, default='Taiwan', max_length=100, null=True),
        ),
    ]
