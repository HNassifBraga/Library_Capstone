# Generated by Django 5.1.5 on 2025-01-31 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isRented',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
