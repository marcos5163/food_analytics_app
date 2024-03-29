# Generated by Django 5.0.1 on 2024-01-31 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_alter_swiggysessiondata_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwiggyOrderTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=100)),
                ('order_total', models.IntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='swiggysessiondata',
            name='session_id',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
