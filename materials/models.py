from django.db import models
from django.core.exceptions import ValidationError
import numpy as np
from django.core.exceptions import ValidationError
from django.db import models
import json

CRYSTAL_STRUCTURE_CHOICES = [
    ("diamond", "diamond"),
    ("zincblende", "zincblende"),
    ("simplecubic", "simplecubic"),
    ("wurtzite", "wurtzite"),
    ("hexagonal", "hexagonal"),
    ("Bi2Te3", "Bi2Te3"),
    ("graphene", "graphene"),
    ("CNT", "CNT"),
    ("buckyball", "buckyball"),
    ("bcc", "bcc"),
    ("caesiumchloride", "caesiumchloride"),
    ("sodiumchloride", "sodiumchloride"),
    ("tetragonal", "tetragonal"),
    ("tetragonalI", "tetragonaLI"),
    ("orthorhombic", "orthorhombic"),
    ("orthorhombicC", "orthorhombicC"),
    ("orthorhombicF", "orthorhombicF"),
    ("orthorhombicI", "orthorhombicI"),
    ("monoclinic", "monoclinic"),
    ("monoclinicC", "monoclinicC"),
    ("triclinic", "triclinic"),
]

DOPING_TYPE_CHOICES = [
    ("N", "N"),
    ("P", "P"),
]

CHARGE_MODEL_CHOICES = [
    ("electron_core", "electron_core"),
    ("electron_hole", "electron_hole"),
]

DOPING_IONIZATION_CHOICES = [
    ("full_ionization", "full_ionization"),
    ("thermal_ionization", "thermal_ionization"),
]

DISORDER_TYPE_CHOICES = [
    ("totally_random_dopant", "totally_random_dopant"),
    ("ordered_dopant", "ordered_dopant"),
]


class Material(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, unique=True)
    regions = models.TextField(default='1,2')
    crystal_structure = models.CharField(max_length=100, choices=CRYSTAL_STRUCTURE_CHOICES)
    
    doping_type = models.CharField(max_length=100, choices=DOPING_TYPE_CHOICES, null=True, blank=True)
    doping_density = models.FloatField(null=True, blank=True)
    charge_model = models.CharField(max_length=100, choices=CHARGE_MODEL_CHOICES, null=True, blank=True)
    doping_ionization_model = models.CharField(max_length=100, choices=DOPING_IONIZATION_CHOICES, null=True, blank=True)
    doping_temperature = models.FloatField(null=True, blank=True)
    ionization_energy = models.FloatField(null=True, blank=True)
    doping_degeneracy = models.FloatField(null=True, blank=True)
    nanotube_indices = models.JSONField(null=True, blank=True)
    disorder_type = models.CharField(max_length=100, choices=DISORDER_TYPE_CHOICES, null=True, blank=True)
    seed = models.IntegerField(null=True, blank=True)
    polarization = models.JSONField(null=True, blank=True)
    strain_simulation = models.BooleanField(default=False)
    
    # Allot specific parameters
    is_alloy = models.BooleanField(default=False)
    mole_fraction = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.tag} - {self.crystal_structure}"
    
    def clean(self):
        # Custom validations
        if self.doping_density is not None and self.doping_density < 0:
            raise ValidationError({'doping_density': 'Doping density must be non-negative.'})
        if self.doping_temperature is not None and self.doping_temperature < 0:
            raise ValidationError({'doping_temperature': 'Doping temperature must be non-negative.'})
        if self.ionization_energy is not None and self.ionization_energy < 0:
            raise ValidationError({'ionization_energy': 'Ionization energy must be non-negative.'})
        if self.doping_degeneracy is not None and self.doping_degeneracy < 0:
            raise ValidationError({'doping_degeneracy': 'Doping degeneracy must be non-negative.'})
        if self.seed is not None and self.seed < 0:
            raise ValidationError({'seed': 'Seed must be non-negative.'})
        if Material.objects.filter(tag__iexact=self.tag).exclude(pk=self.pk).exists():
            raise ValidationError({'tag': 'This tag is already in use. Please choose a different one.'})
        super(Material, self).clean()
