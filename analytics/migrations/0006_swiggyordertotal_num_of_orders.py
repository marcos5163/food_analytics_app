# Generated by Django 5.0.1 on 2024-01-31 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_swiggyordertotal_alter_swiggysessiondata_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='swiggyordertotal',
            name='num_of_orders',
            field=models.IntegerField(null=True),
        ),
    ]
