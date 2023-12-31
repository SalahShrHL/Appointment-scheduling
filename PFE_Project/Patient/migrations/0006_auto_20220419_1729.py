# Generated by Django 3.2.9 on 2022-04-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0005_auto_20220419_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_naiss',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rv',
            name='status',
            field=models.CharField(choices=[('confirmé', 'confirmé'), ('non_confirmé', 'non_confirmé')], max_length=15),
        ),
    ]
