# Generated by Django 3.2.4 on 2022-01-07 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job',
            field=models.CharField(choices=[('student', '學生'), ('employed', '在職'), ('other', '其他')], default='other', max_length=100),
        ),
    ]