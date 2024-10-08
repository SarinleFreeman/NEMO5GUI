# Generated by Django 5.0.7 on 2024-08-15 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boundarycondition',
            name='solver_name',
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='E_field',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='boundary_regions',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='metal_work_function',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='potential_simulation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='boundarycondition',
            name='semiconductor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boundarycondition',
            name='single_surface_normal',
            field=models.CharField(blank=True, help_text='Enter the normal to the surface as comma-separated values (x,y,z)', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='boundarycondition',
            name='surface_of_regions',
            field=models.CharField(help_text='Enter the name or number of the region(s)', max_length=50),
        ),
        migrations.AlterField(
            model_name='boundarycondition',
            name='type',
            field=models.CharField(choices=[('ElectrostaticContact', 'Electrostatic Contact'), ('PotentialFromSolver', 'Potential From Solver'), ('NormalField', 'Normal Field'), ('OhmicContact', 'Ohmic Contact'), ('SchottkyContact', 'Schottky Contact')], max_length=50),
        ),
        migrations.AlterField(
            model_name='boundarycondition',
            name='voltage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
