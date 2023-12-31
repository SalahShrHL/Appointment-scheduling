# Generated by Django 3.2.9 on 2022-05-02 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0013_remove_cabinet_commune'),
    ]

    operations = [
        migrations.AddField(
            model_name='motif',
            name='end',
            field=models.TimeField(default='0:0'),
        ),
        migrations.AddField(
            model_name='motif',
            name='start',
            field=models.TimeField(default='0:0'),
        ),
        migrations.AlterField(
            model_name='motif',
            name='duree',
            field=models.PositiveIntegerField(choices=[('3', 15), ('2', 10), ('1', 5), ('4', 20), ('7', 60), ('5', 30), ('6', 45)]),
        ),
        migrations.RemoveField(
            model_name='motif',
            name='jours',
        ),
        migrations.AddField(
            model_name='motif',
            name='jours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.jour'),
        ),
    ]
