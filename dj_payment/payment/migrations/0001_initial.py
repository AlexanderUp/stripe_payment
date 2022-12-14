# Generated by Django 4.1.1 on 2022-09-13 12:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Item name', max_length=255, unique=True, verbose_name='Item name')),
                ('description', models.CharField(help_text='Item description', max_length=255, verbose_name='Item description')),
                ('price', models.FloatField(help_text='Item price', validators=[django.core.validators.MinValueValidator(0, message='Price cannot be negative.')], verbose_name='Item price')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
    ]
