# Generated by Django 3.1.2 on 2020-12-02 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ihelprapp', '0023_remove_sitter_post_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='attached_file',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
