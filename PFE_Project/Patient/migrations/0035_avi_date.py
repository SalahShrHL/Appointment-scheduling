# Generated by Django 3.2.9 on 2022-05-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0034_auto_20220528_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='avi',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]