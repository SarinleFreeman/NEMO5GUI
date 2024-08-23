from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
import numpy as np

class RegionShape(models.TextChoices):
    CUBOID = 'Cuboid', 'Cuboid'
    SPHEROID = 'Spheroid', 'Spheroid'
    PYRAMID = 'Pyramid', 'Pyramid'
    CYLINDER = 'Cylinder', 'Cylinder'
    DOME = 'Dome', 'Dome'
    twod = '2d', '2d'


class BaseRegion(models.Model):
    shape = models.CharField(max_length=10, choices=RegionShape.choices)
    tag = models.CharField(
        max_length=100, 
        unique=True,
        validators=[RegexValidator(
            regex='^[A-Za-z0-9]+$',
            message='Tag must be alphanumeric.',
            code='invalid_tag'
        )]
    )
    region_number = models.IntegerField(
        validators=[MinValueValidator(1)],
        unique=True
    )
    priority = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        abstract = True

class Region(BaseRegion):
    min_x = models.FloatField()
    min_y = models.FloatField()
    min_z = models.FloatField()
    max_x = models.FloatField()
    max_y = models.FloatField()
    max_z = models.FloatField()


    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(region_number__gte=1), name='region_number_gte_1'),
            models.CheckConstraint(check=models.Q(priority__gte=1), name='priority_gte_1')
        ]

class BoundaryRegion(BaseRegion):
    work_plane = models.CharField(max_length=1, choices=[('X', 'X'), ('Y', 'Y'), ('Z', 'Z')])
    plane_tolerance = models.FloatField()
    axis_cut = models.IntegerField()
    rectangles = models.JSONField(default=list)  # Storing list of rectangles as JSON

    def clean(self):
        super().clean()
        if self.plane_tolerance < 0:
            raise ValidationError({'plane_tolerance': 'Plane tolerance must be a positive number.'})
        
        # Validate rectangles
        if not isinstance(self.rectangles, list):
            raise ValidationError({'rectangles': 'Rectangles must be a list.'})
        
        for rect in self.rectangles:
            if not isinstance(rect, list) or len(rect) != 5:
                raise ValidationError({'rectangles': 'Each rectangle must be a list of 5 elements.'})
            
            region_id, x, y, width, height = rect
            if region_id != self.region_number:
                raise ValidationError({'rectangles': f'Rectangle ID {region_id} does not match region number {self.region_number}.'})
            
            if not all(isinstance(val, (int, float)) for val in rect):
                raise ValidationError({'rectangles': 'All rectangle values must be numbers.'})
            
            if width <= 0 or height <= 0:
                raise ValidationError({'rectangles': 'Width and height must be positive.'})