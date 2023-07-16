# Generated by Django 3.2.9 on 2022-05-29 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0035_avi_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='rv',
            name='Patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.patient'),
        ),
        migrations.AlterField(
            model_name='medecinfavori',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.patient'),
        ),
    ]