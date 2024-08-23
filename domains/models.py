from django.db import models
import json

class Domain(models.Model):
    ELEMENT_CHOICES = [
        ('cuboid8', 'Cuboid8'),
        ('cuboid27', 'Cuboid27'),
        ('cuboid20', 'Cuboid20'),
        ('tetrahedron4', 'Tetrahedron4'),
        ('tetrahedron10', 'Tetrahedron10'),
        ('pyramid5', 'Pyramid5'),
        ('prism6', 'Prism6'),
        ('prism15', 'Prism15'),
        ('prism18', 'Prism18'),
        ('quad4', 'Quad4'),
        ('quad8', 'Quad8'),
        ('quad9', 'Quad9'),
        ('tri3', 'Tri3'),
        ('tri6', 'Tri6'),
        ('edge2', 'Edge2'),
        ('edge3', 'Edge3'),
        ('edge4', 'Edge4'),
        ('node1', 'Node1'),
    ]

    name = models.CharField(max_length=100, help_text="The unique name of the domain.")
    domain_type = models.CharField(max_length=100, default="FEM_macroscopic", help_text="The type of domain, defaults to 'FEM_macroscopic' for finite element method.")
    regions = models.TextField(help_text="list of integers representing different regions within the domain.")
    mesh_dimension = models.IntegerField(default=3, help_text="The dimension of the mesh (1D, 2D, 3D).")

    # Mesh parameters
    xmin = models.FloatField(null=True, blank=True, help_text="Minimum x-coordinate boundary of the mesh.")
    xmax = models.FloatField(null=True, blank=True, help_text="Maximum x-coordinate boundary of the mesh.")
    ymin = models.FloatField(null=True, blank=True, help_text="Minimum y-coordinate boundary of the mesh.")
    ymax = models.FloatField(null=True, blank=True, help_text="Maximum y-coordinate boundary of the mesh.")
    zmin = models.FloatField(null=True, blank=True, help_text="Minimum z-coordinate boundary of the mesh.")
    zmax = models.FloatField(null=True, blank=True, help_text="Maximum z-coordinate boundary of the mesh.")
    nx = models.IntegerField(null=True, blank=True, help_text="Number of divisions in the x-direction.")
    ny = models.IntegerField(null=True, blank=True, help_text="Number of divisions in the y-direction.")
    nz = models.IntegerField(null=True, blank=True, help_text="Number of divisions in the z-direction.")
    dx = models.FloatField(null=True, blank=True, help_text="Mesh grid spacing in the x-direction.")
    dy = models.FloatField(null=True, blank=True, help_text="Mesh grid spacing in the y-direction.")
    dz = models.FloatField(null=True, blank=True, help_text="Mesh grid spacing in the z-direction.")
    element_kind = models.CharField(max_length=20, choices=ELEMENT_CHOICES, default='cuboid8', help_text="Type of element used in the mesh.")

    # Mesh generation options
    import_from_file = models.TextField(null=True, blank=True, help_text="Path to a file from which the mesh is imported.")
    submesh_from_domain = models.TextField(null=True, blank=True, help_text="Name of another domain from which a submesh is derived.")
    nonorthogonal_mesh = models.BooleanField(default=False, help_text="Flag to indicate if the mesh is nonorthogonal.")
    mesh_vector1 = models.TextField(null=True, blank=True, help_text="Enter the first vector as comma-separated values, e.g., '1.0, 0.0, 0.0'")
    mesh_vector2 = models.TextField(null=True, blank=True, help_text="Enter the second vector as comma-separated values, e.g., '0.0, 1.0, 0.0'")
    mesh_vector3 = models.TextField(null=True, blank=True, help_text="Enter the third vector as comma-separated values, e.g., '0.0, 0.0, 1.0'")
    # Refinement
    number_of_refinement_steps = models.IntegerField(null=True, default=0, help_text="Number of refinement steps to be applied to the mesh.")

    # Atomistic coupling
    atomistic_domains = models.CharField(max_length=255, null=True, blank=True, help_text="Associated atomistic domains if any.")
    automatic_minimal_point_on_atom = models.BooleanField(null=True,default=False, help_text="Automatically calculate the minimal point on the atomic domain.")

    # Other options
    sanity_check = models.BooleanField(null=True,default=True, help_text="Perform a sanity check during operations.")

    # Parallelization section
    parallel = models.BooleanField(null=True,default=False, help_text="Enable parallel domain operations.")
    xmin_p = models.FloatField(null=True, blank=True, help_text="Minimum x-coordinate of the cuboid enclosing the structure.")
    xmax_p = models.FloatField(null=True, blank=True, help_text="Maximum x-coordinate of the cuboid enclosing the structure.")
    ymin_p = models.FloatField(null=True, blank=True, help_text="Minimum y-coordinate of the cuboid enclosing the structure.")
    ymax_p = models.FloatField(null=True, blank=True, help_text="Maximum y-coordinate of the cuboid enclosing the structure.")
    zmin_p = models.FloatField(null=True, blank=True, help_text="Minimum z-coordinate of the cuboid enclosing the structure.")
    zmax_p = models.FloatField(null=True, blank=True, help_text="Maximum z-coordinate of the cuboid enclosing the structure.")
    num_geom_cpus = models.IntegerField(null=True, blank=True, help_text="Number of CPUs used for geometry-related computations.")


    def __str__(self):
        return f"{self.name} - {self.domain_type}"