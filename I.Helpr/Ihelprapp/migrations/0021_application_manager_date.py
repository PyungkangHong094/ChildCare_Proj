# Generated by Django 3.1.2 on 2020-11-30 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ihelprapp', '0020_remove_application_manager_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='application_manager',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_column='date', null=True),
        ),
    ]
