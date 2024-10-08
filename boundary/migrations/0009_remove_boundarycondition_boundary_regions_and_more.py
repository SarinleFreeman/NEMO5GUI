# Generated by Django 5.0.7 on 2024-08-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundary', '0008_alter_boundarycondition_options_and_more'),
        ('regions', '0003_alter_boundaryregion_shape_alter_region_shape'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boundarycondition',
            name='boundary_regions',
        ),
        migrations.RemoveField(
            model_name='boundarycondition',
            name='surface_of_regions',
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='surface_of_regions',
            field=models.ManyToManyField(blank=True, related_name='boundary_conditions', to='regions.region'),
        ),
    ]
