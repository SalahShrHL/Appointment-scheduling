# Generated by Django 3.2.9 on 2022-05-19 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0025_rv_valide_heure'),
    ]

    operations = [
        migrations.AddField(
            model_name='rv_valide',
            name='nom_payer',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='rv_valide',
            name='num_carte',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='rv_valide',
            name='prenom_payer',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
