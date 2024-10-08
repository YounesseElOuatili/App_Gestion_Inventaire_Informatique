# Generated by Django 5.0.7 on 2024-08-27 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_alter_produit_etat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='date_achat',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='valeur_achat',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
