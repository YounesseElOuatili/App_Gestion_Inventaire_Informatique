# Generated by Django 5.0.7 on 2024-08-27 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0009_produit_date_achat_produit_etat_produit_valeur_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='etat',
            field=models.CharField(choices=[('en_service', 'En service'), ('en_stock', 'En stock'), ('en_cours_de_maintenance', 'En cours de maintenance'), ('hors_service', 'Hors service')], default='en_service', max_length=50),
        ),
    ]
