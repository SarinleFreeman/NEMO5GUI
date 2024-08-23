from django import forms
from .models import BoundaryCondition, BoundaryConditionType
from regions.models import Region
from materials.models import Material

class BoundaryConditionForm(forms.ModelForm):
    class Meta:
        model = BoundaryCondition
        fields = ['name','solver_model_name', 'type', 'voltage', 'single_surface_normal',
                  'metal_work_function', 'semiconductor', 'surface_of_regions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make type a dropdown
        self.fields['type'] = forms.ChoiceField(
            choices=BoundaryConditionType.choices,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        # Update surface_of_regions field to use SelectMultiple with a "No Regions Exist" option if empty
        regions_queryset = Region.objects.all().order_by('region_number')
        if not regions_queryset.exists():
            self.fields['surface_of_regions'] = forms.ChoiceField(
                choices=[('', 'NO REGIONS EXIST')],
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False
            )
        else:
            self.fields['surface_of_regions'] = forms.ModelMultipleChoiceField(
                queryset=regions_queryset,
                widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
                required=False
            )

        # Update semiconductor field to use ModelChoiceField with a "No Materials Exist" option if empty
        materials_queryset = Material.objects.all()
        if not materials_queryset.exists():
            self.fields['semiconductor'] = forms.ChoiceField(
                choices=[('', 'NO MATERIALS EXIST')],
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False
            )
        else:
            self.fields['semiconductor'] = forms.ModelChoiceField(
                queryset=materials_queryset,
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False
            )


        # Add some basic styling and make all fields not required
        for field in self.fields:
            self.fields[field].required = False
            if isinstance(self.fields[field].widget, forms.widgets.Input):
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        boundary_condition_type = cleaned_data.get('type')

        if not cleaned_data.get('solver_model_name'):
                self.add_error('solver_model_name', 'Solver model name is required.')

        if boundary_condition_type == BoundaryConditionType.SCHOTTKY_CONTACT:
            # Validate fields specific to Schottky Contact
            if not cleaned_data.get('metal_work_function'):
                self.add_error('metal_work_function', 'Metal work function is required for Schottky Contact.')
            if not cleaned_data.get('semiconductor'):
                self.add_error('semiconductor', 'Semiconductor is required for Schottky Contact.')
            if not cleaned_data.get('surface_of_regions') or cleaned_data.get('surface_of_regions').count() == 0:
                self.add_error('surface_of_regions', 'At least one region is required for Schottky Contact.')
            if not cleaned_data.get('single_surface_normal'):
                self.add_error('single_surface_normal', 'Single surface normal is required for Schottky Contact.')

        elif boundary_condition_type == BoundaryConditionType.ELECTROSTATIC_CONTACT:
            # Validate fields specific to Electrostatic Contact
            if not cleaned_data.get('voltage'):
                self.add_error('voltage', 'Voltage is required for Electrostatic Contact.')
            if not cleaned_data.get('surface_of_regions'):
                self.add_error('surface_of_regions', 'Surface of regions is required for Electrostatic Contact.')
            if not cleaned_data.get('single_surface_normal'):
                self.add_error('single_surface_normal', 'Single surface normal is required for Electrostatic Contact.')

        else:
            self.add_error('type', 'Invalid boundary condition type.')

        return cleaned_data