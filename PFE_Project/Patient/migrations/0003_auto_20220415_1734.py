# Generated by Django 3.2.9 on 2022-04-15 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0002_alter_cabinet_commune'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet',
            name='wilaya',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.wilaya'),
        ),
        migrations.AlterField(
            model_name='rv',
            name='status',
            field=models.CharField(choices=[('non_confirmé', 'non_confirmé'), ('confirmé', 'confirmé')], max_length=15),
        ),
    ]
