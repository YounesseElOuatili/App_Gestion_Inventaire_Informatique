# Generated by Django 5.0.7 on 2024-08-08 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_delete_historicalsociete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsite',
            name='patente',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='ref',
        ),
        migrations.RemoveField(
            model_name='historicalsite',
            name='societe_obj',
        ),
        migrations.RemoveField(
            model_name='site',
            name='patente',
        ),
        migrations.RemoveField(
            model_name='site',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='site',
            name='ref',
        ),
        migrations.RemoveField(
            model_name='site',
            name='societe_obj',
        ),
    ]
