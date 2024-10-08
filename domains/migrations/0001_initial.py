# Generated by Django 5.0.7 on 2024-08-14 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The unique name of the domain.', max_length=100)),
                ('domain_type', models.CharField(default='FEM', help_text="The type of domain, defaults to 'FEM' for finite element method.", max_length=100)),
                ('regions', models.TextField(help_text='list of integers representing different regions within the domain.')),
                ('mesh_dimension', models.IntegerField(default=3, help_text='The dimension of the mesh (1D, 2D, 3D).')),
                ('xmin', models.FloatField(blank=True, help_text='Minimum x-coordinate boundary of the mesh.', null=True)),
                ('xmax', models.FloatField(blank=True, help_text='Maximum x-coordinate boundary of the mesh.', null=True)),
                ('ymin', models.FloatField(blank=True, help_text='Minimum y-coordinate boundary of the mesh.', null=True)),
                ('ymax', models.FloatField(blank=True, help_text='Maximum y-coordinate boundary of the mesh.', null=True)),
                ('zmin', models.FloatField(blank=True, help_text='Minimum z-coordinate boundary of the mesh.', null=True)),
                ('zmax', models.FloatField(blank=True, help_text='Maximum z-coordinate boundary of the mesh.', null=True)),
                ('nx', models.IntegerField(blank=True, help_text='Number of divisions in the x-direction.', null=True)),
                ('ny', models.IntegerField(blank=True, help_text='Number of divisions in the y-direction.', null=True)),
                ('nz', models.IntegerField(blank=True, help_text='Number of divisions in the z-direction.', null=True)),
                ('dx', models.FloatField(blank=True, help_text='Mesh grid spacing in the x-direction.', null=True)),
                ('dy', models.FloatField(blank=True, help_text='Mesh grid spacing in the y-direction.', null=True)),
                ('dz', models.FloatField(blank=True, help_text='Mesh grid spacing in the z-direction.', null=True)),
                ('element_kind', models.CharField(choices=[('cuboid8', 'Cuboid8'), ('cuboid27', 'Cuboid27'), ('cuboid20', 'Cuboid20'), ('tetrahedron4', 'Tetrahedron4'), ('tetrahedron10', 'Tetrahedron10'), ('pyramid5', 'Pyramid5'), ('prism6', 'Prism6'), ('prism15', 'Prism15'), ('prism18', 'Prism18'), ('quad4', 'Quad4'), ('quad8', 'Quad8'), ('quad9', 'Quad9'), ('tri3', 'Tri3'), ('tri6', 'Tri6'), ('edge2', 'Edge2'), ('edge3', 'Edge3'), ('edge4', 'Edge4'), ('node1', 'Node1')], default='cuboid8', help_text='Type of element used in the mesh.', max_length=20)),
                ('import_from_file', models.TextField(blank=True, help_text='Path to a file from which the mesh is imported.', null=True)),
                ('submesh_from_domain', models.TextField(blank=True, help_text='Name of another domain from which a submesh is derived.', null=True)),
                ('nonorthogonal_mesh', models.BooleanField(default=False, help_text='Flag to indicate if the mesh is nonorthogonal.')),
                ('mesh_vector1', models.TextField(blank=True, help_text="Enter the first vector as comma-separated values, e.g., '1.0, 0.0, 0.0'", null=True)),
                ('mesh_vector2', models.TextField(blank=True, help_text="Enter the second vector as comma-separated values, e.g., '0.0, 1.0, 0.0'", null=True)),
                ('mesh_vector3', models.TextField(blank=True, help_text="Enter the third vector as comma-separated values, e.g., '0.0, 0.0, 1.0'", null=True)),
                ('number_of_refinement_steps', models.IntegerField(default=0, help_text='Number of refinement steps to be applied to the mesh.', null=True)),
                ('atomistic_domains', models.CharField(blank=True, help_text='Associated atomistic domains if any.', max_length=255, null=True)),
                ('automatic_minimal_point_on_atom', models.BooleanField(default=False, help_text='Automatically calculate the minimal point on the atomic domain.', null=True)),
                ('sanity_check', models.BooleanField(default=True, help_text='Perform a sanity check during operations.', null=True)),
                ('parallel', models.BooleanField(default=False, help_text='Enable parallel domain operations.', null=True)),
                ('xmin_p', models.FloatField(blank=True, help_text='Minimum x-coordinate of the cuboid enclosing the structure.', null=True)),
                ('xmax_p', models.FloatField(blank=True, help_text='Maximum x-coordinate of the cuboid enclosing the structure.', null=True)),
                ('ymin_p', models.FloatField(blank=True, help_text='Minimum y-coordinate of the cuboid enclosing the structure.', null=True)),
                ('ymax_p', models.FloatField(blank=True, help_text='Maximum y-coordinate of the cuboid enclosing the structure.', null=True)),
                ('zmin_p', models.FloatField(blank=True, help_text='Minimum z-coordinate of the cuboid enclosing the structure.', null=True)),
                ('zmax_p', models.FloatField(blank=True, help_text='Maximum z-coordinate of the cuboid enclosing the structure.', null=True)),
                ('num_geom_cpus', models.IntegerField(blank=True, help_text='Number of CPUs used for geometry-related computations.', null=True)),
            ],
        ),
    ]
