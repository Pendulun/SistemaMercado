# Generated by Django 4.0.4 on 2022-05-28 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('brand', models.CharField(max_length=255)),
                ('stock', models.PositiveIntegerField()),
                ('sold', models.PositiveIntegerField()),
            ],
        ),
    ]
