# Generated by Django 5.0.7 on 2024-08-12 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_categorie_produits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorie',
            name='produits',
        ),
    ]
