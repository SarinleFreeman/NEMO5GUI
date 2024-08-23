from django import forms
from .models import Domain

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'required': True,
                'pattern': '[A-Za-z0-9 ]+',
                'placeholder': 'Enter domain name',
                'class': 'form-control'
            }),
            'domain_type': forms.TextInput(attrs={
                'readonly': True,  # Assuming domain_type is predefined and not editable
                'class': 'form-control'
            }),
            'regions': forms.TextInput(attrs={'placeholder': 'Enter comma-separated region IDs'}),

            'mesh_dimension': forms.NumberInput(attrs={
                'min': 1,
                'max': 3,
                'required': True,
                'class': 'form-control'
            }),
            'xmin': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Minimum x-coordinate'
            }),
            'xmax': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Maximum x-coordinate'
            }),
            'ymin': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Minimum y-coordinate'
            }),
            'ymax': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Maximum y-coordinate'
            }),
            'zmin': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Minimum z-coordinate'
            }),
            'zmax': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Maximum z-coordinate'
            }),
            'nx': forms.NumberInput(attrs={
                'min': 0, 
                'class': 'form-control', 
                'placeholder': 'Divisions along x-axis'
            }),
            'ny': forms.NumberInput(attrs={
                'min': 0, 
                'class': 'form-control', 
                'placeholder': 'Divisions along y-axis'
            }),
            'nz': forms.NumberInput(attrs={
                'min': 0, 
                'class': 'form-control', 
                'placeholder': 'Divisions along z-axis'
            }),
            'dx': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Grid spacing in x-direction'
            }),
            'dy': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Grid spacing in y-direction'
            }),
            'dz': forms.NumberInput(attrs={
                'step': 'any', 
                'class': 'form-control', 
                'placeholder': 'Grid spacing in z-direction'
            }),
            'element_kind': forms.Select(attrs={'class': 'form-control'}),
            'import_from_file': forms.Textarea(attrs={
                'placeholder': 'Enter the file path for mesh import',
                'class': 'form-control',
                'rows': 1  # You can specify fewer rows if the text field does not need to be large
            }),
            'submesh_from_domain': forms.Textarea(attrs={
                'placeholder': 'Enter the domain name for submesh derivation',
                'class': 'form-control',
                'rows': 1  # Adjust the number of rows according to your UI design
            }),
            'nonorthogonal_mesh': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mesh_vector1': forms.TextInput(attrs={
            'placeholder': 'e.g., 1.0, 0.0, 0.0',
            'class': 'form-control'
            }),
            'mesh_vector2': forms.TextInput(attrs={
                'placeholder': 'e.g., 0.0, 1.0, 0.0',
                'class': 'form-control'
            }),
            'mesh_vector3': forms.TextInput(attrs={
                'placeholder': 'e.g., 0.0, 0.0, 1.0',
                'class': 'form-control'
            }),
            'number_of_refinement_steps': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control'
            }),
            'atomistic_domains': forms.TextInput(attrs={
                'placeholder': 'Associated atomistic domains, if any',
                'class': 'form-control'
            }),
            'automatic_minimal_point_on_atom': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sanity_check': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parallel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'xmin_p': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter minimum x-extension'
            }),
            'xmax_p': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter maximum x-extension'
            }),
            'ymin_p': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter minimum y-extension'
            }),
            'ymax_p': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter maximum y-extension'
            }),
            'zmin_p': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter minimum z-extension'
            }),
            'zmax_p': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter maximum z-extension'
            }), 
            'num_geom_cpus': forms.NumberInput(attrs={
                'min': 1,
                'placeholder': 'Number of CPUs',
                'class': 'form-control'
            }),
        }