from django.db import models
from regions.models import Region
from materials.models import Material

class BoundaryConditionType(models.TextChoices):
    ELECTROSTATIC_CONTACT = 'ElectrostaticContact', 'Electrostatic Contact'
    SCHOTTKY_CONTACT = 'SchottkyContact', 'Schottky Contact'

class BoundaryCondition(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Make the name field unique
    solver_model_name = models.CharField(max_length=100)
    surface_of_regions = models.ManyToManyField(Region, related_name='boundary_conditions', blank=True)
    type = models.CharField(max_length=50, choices=BoundaryConditionType.choices)
    voltage = models.FloatField(null=True, blank=True)
    single_surface_normal = models.CharField(max_length=20, default="1,0,0")

    # Fields specific to SchottkyContact
    metal_work_function = models.FloatField(null=True, blank=True)
    semiconductor = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Boundary Condition"
        verbose_name_plural = "Boundary Conditions"