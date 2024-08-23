# Generated by Django 5.0.7 on 2024-08-14 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoundaryCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('ElectrostaticContact', 'Electrostatic Contact')], default='ElectrostaticContact', max_length=50)),
                ('voltage', models.FloatField()),
                ('surface_of_regions', models.CharField(help_text='Enter the name of the region', max_length=50)),
                ('single_surface_normal', models.CharField(help_text='Enter the normal to the surface as comma-separated values (x,y,z)', max_length=50)),
                ('solver_name', models.CharField(max_length=100)),
            ],
        ),
    ]
