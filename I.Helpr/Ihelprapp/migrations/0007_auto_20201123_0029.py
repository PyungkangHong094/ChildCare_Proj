# Generated by Django 3.1.2 on 2020-11-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ihelprapp', '0006_auto_20201122_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_status',
        ),
        migrations.AddField(
            model_name='message_hitory',
            name='message_status',
            field=models.CharField(choices=[('R', 'Read'), ('U', 'Unread')], db_column='message_status', default='U', max_length=1),
        ),
    ]