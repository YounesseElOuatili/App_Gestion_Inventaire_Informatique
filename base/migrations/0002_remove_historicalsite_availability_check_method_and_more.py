# Generated by Django 4.2.3 on 2024-07-24 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsite',
            name='availability_check_method',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='expected_exit_time',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='max_delivery_number',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='max_duration',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='taux_dt',
        ),
        migrations.RemoveField(
            model_name='site',
            name='availability_check_method',
        ),
        migrations.RemoveField(
            model_name='site',
            name='expected_exit_time',
        ),
        migrations.RemoveField(
            model_name='site',
            name='max_delivery_number',
        ),
        migrations.RemoveField(
            model_name='site',
            name='max_duration',
        ),
        migrations.RemoveField(
            model_name='site',
            name='taux_dt',
        ),
    ]
