# Generated by Django 5.1.7 on 2025-03-24 09:36

import GridSense.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementsFive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.PositiveIntegerField()),
                ('sensdata', GridSense.models.NestedDecimalArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=5), size=2), size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rmsvalue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Power Factor')),
                ('thd', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Total Harmonic Distortion')),
                ('sname', models.CharField(max_length=50, verbose_name='Sensor Name')),
                ('stype', models.CharField(choices=[('Current', 'Current'), ('Voltage', 'Voltage')], max_length=50, verbose_name='Sensor Type')),
            ],
            options={
                'db_table': 'measurements_five',
            },
        ),
        migrations.CreateModel(
            name='MeasurementsFour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.PositiveIntegerField()),
                ('sensdata', GridSense.models.NestedDecimalArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=5), size=2), size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rmsvalue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Power Factor')),
                ('thd', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Total Harmonic Distortion')),
                ('sname', models.CharField(max_length=50, verbose_name='Sensor Name')),
                ('stype', models.CharField(choices=[('Current', 'Current'), ('Voltage', 'Voltage')], max_length=50, verbose_name='Sensor Type')),
            ],
            options={
                'db_table': 'measurements_four',
            },
        ),
        migrations.CreateModel(
            name='MeasurementsOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.PositiveIntegerField()),
                ('sensdata', GridSense.models.NestedDecimalArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=5), size=2), size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rmsvalue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Power Factor')),
                ('thd', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Total Harmonic Distortion')),
                ('sname', models.CharField(max_length=50, verbose_name='Sensor Name')),
                ('stype', models.CharField(choices=[('Current', 'Current'), ('Voltage', 'Voltage')], max_length=50, verbose_name='Sensor Type')),
            ],
            options={
                'db_table': 'measurements_one',
            },
        ),
        migrations.CreateModel(
            name='MeasurementsSix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.PositiveIntegerField()),
                ('sensdata', GridSense.models.NestedDecimalArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=5), size=2), size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rmsvalue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Power Factor')),
                ('thd', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Total Harmonic Distortion')),
                ('sname', models.CharField(max_length=50, verbose_name='Sensor Name')),
                ('stype', models.CharField(choices=[('Current', 'Current'), ('Voltage', 'Voltage')], max_length=50, verbose_name='Sensor Type')),
            ],
            options={
                'db_table': 'measurements_six',
            },
        ),
        migrations.CreateModel(
            name='MeasurementsThree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.PositiveIntegerField()),
                ('sensdata', GridSense.models.NestedDecimalArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=5), size=2), size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rmsvalue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Power Factor')),
                ('thd', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Total Harmonic Distortion')),
                ('sname', models.CharField(max_length=50, verbose_name='Sensor Name')),
                ('stype', models.CharField(choices=[('Current', 'Current'), ('Voltage', 'Voltage')], max_length=50, verbose_name='Sensor Type')),
            ],
            options={
                'db_table': 'measurements_three',
            },
        ),
        migrations.CreateModel(
            name='MeasurementsTwo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.PositiveIntegerField()),
                ('sensdata', GridSense.models.NestedDecimalArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=5), size=2), size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rmsvalue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Power Factor')),
                ('thd', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Total Harmonic Distortion')),
                ('sname', models.CharField(max_length=50, verbose_name='Sensor Name')),
                ('stype', models.CharField(choices=[('Current', 'Current'), ('Voltage', 'Voltage')], max_length=50, verbose_name='Sensor Type')),
            ],
            options={
                'db_table': 'measurements_two',
            },
        ),
    ]
