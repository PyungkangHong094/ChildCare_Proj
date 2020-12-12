# Generated by Django 3.1.2 on 2020-11-30 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ihelprapp', '0017_auto_20201129_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_column='date', null=True),
        ),
        migrations.AddField(
            model_name='application_manager',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ihelprapp.application'),
        ),
        migrations.AddField(
            model_name='application_manager',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_column='date', null=True),
        ),
        migrations.AddField(
            model_name='application_manager',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ihelprapp.parent_post'),
        ),
        migrations.AlterUniqueTogether(
            name='application_manager',
            unique_together={('post', 'application')},
        ),
        migrations.RemoveField(
            model_name='application_manager',
            name='application_id',
        ),
        migrations.RemoveField(
            model_name='application_manager',
            name='post_id',
        ),
    ]