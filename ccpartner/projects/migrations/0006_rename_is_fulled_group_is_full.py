# Generated by Django 3.2.4 on 2021-12-25 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20211225_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='is_fulled',
            new_name='is_full',
        ),
    ]
