# Generated by Django 4.1.2 on 2022-11-11 17:01

from django.db import migrations, models
import storeapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(db_index=True, default=storeapp.models.generate_random_code, max_length=20),
        ),
    ]
