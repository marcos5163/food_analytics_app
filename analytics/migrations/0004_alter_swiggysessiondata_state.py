# Generated by Django 5.0.1 on 2024-01-31 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_alter_swiggysessiondata_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swiggysessiondata',
            name='state',
            field=models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('EXPIRED', 'EXPIRED')], default='ACTIVE', max_length=100),
        ),
    ]