# Generated by Django 3.2.9 on 2022-04-24 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0009_remove_patient_commune'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet',
            name='NomCabinet',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='date_naiss',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='genre',
            field=models.CharField(blank=True, choices=[('female', 'female'), ('male', 'male')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='rating',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='specialite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.specialite'),
        ),
    ]
