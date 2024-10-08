# Generated by Django 5.0.7 on 2024-08-15 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundary', '0003_remove_boundarycondition_boundary_regions_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boundarycondition',
            name='regions',
        ),
        migrations.RemoveField(
            model_name='boundarycondition',
            name='semiconductor_materials',
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='boundary_regions',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='semiconductor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='surface_of_regions',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boundarycondition',
            name='single_surface_normal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boundarycondition',
            name='type',
            field=models.CharField(choices=[('ElectrostaticContact', 'Electrostatic Contact'), ('PotentialFromSolver', 'Potential From Solver'), ('NormalField', 'Normal Field'), ('SchottkyContact', 'Schottky Contact')], max_length=50),
        ),
    ]
