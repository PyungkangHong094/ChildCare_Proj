# Generated by Django 3.1.2 on 2020-12-02 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ihelprapp', '0022_auto_20201201_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitter_post',
            name='application',
        ),
    ]