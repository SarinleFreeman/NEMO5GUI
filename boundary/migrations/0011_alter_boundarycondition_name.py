# Generated by Django 5.0.7 on 2024-08-22 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundary', '0010_boundarycondition_solver_model_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boundarycondition',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
