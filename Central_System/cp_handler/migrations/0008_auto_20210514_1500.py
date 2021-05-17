# Generated by Django 3.2.2 on 2021-05-14 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp_handler', '0007_alter_idtaginfo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargepoint',
            name='chargePointModel',
            field=models.CharField(default='Elvi', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chargepoint',
            name='chargePointVendor',
            field=models.CharField(default='EVBox', max_length=256),
            preserve_default=False,
        ),
    ]
