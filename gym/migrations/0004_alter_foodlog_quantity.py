# Generated by Django 5.0.7 on 2024-11-01 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0003_foodlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodlog',
            name='quantity',
            field=models.CharField(max_length=50),
        ),
    ]