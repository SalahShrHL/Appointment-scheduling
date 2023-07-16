# Generated by Django 3.2.9 on 2022-05-03 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0016_auto_20220503_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motif',
            name='Cabinet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.cabinet'),
        ),
        migrations.AlterField(
            model_name='motif',
            name='duree',
            field=models.PositiveIntegerField(choices=[('1', 5), ('3', 15), ('6', 45), ('4', 20), ('7', 60), ('5', 30), ('2', 10)]),
        ),
        migrations.AlterField(
            model_name='rv',
            name='status',
            field=models.CharField(choices=[('non_confirmé', 'non_confirmé'), ('confirmé', 'confirmé')], max_length=15),
        ),
    ]