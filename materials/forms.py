from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'pattern': '[A-Za-z0-9 ]+', 'placeholder': 'Enter material name'}),
            'tag': forms.TextInput(attrs={'required': True, 'pattern': '[A-Za-z0-9]+', 'placeholder': 'Unique material tag'}),
            'regions': forms.TextInput(attrs={'placeholder': 'Enter comma-separated region IDs'}),
            'crystal_structure': forms.Select(attrs={'required': True}),
            'doping_type': forms.Select(attrs={'required': False}),
            'doping_density': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'required': False, 'placeholder': 'Enter doping density (cm^3)'}),
            'charge_model': forms.Select(attrs={'required': False}),
            'doping_ionization_model': forms.Select(attrs={'required': False}),
            'doping_temperature': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'required': False, 'placeholder': 'Enter doping temperature (Kelvin)'}),
            'ionization_energy': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'required': False, 'placeholder': 'Enter ionization energy (eV)'}),
            'doping_degeneracy': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'required': False, 'placeholder': 'Enter doping degeneracy'}),
            'nanotube_indices': forms.Textarea(attrs={'cols': 40, 'rows': 1, 'placeholder': 'Enter indices e.g., [5, 10]'}),
            'additional_params': forms.Textarea(attrs={'cols': 40, 'rows': 3, 'placeholder': 'JSON format'}),
            'disorder_type': forms.Select(attrs={'required': False}),
            'seed': forms.NumberInput(attrs={'min': 0, 'required': False, 'placeholder': 'Enter seed'}),
            'polarization': forms.Textarea(attrs={'cols': 40, 'rows': 1, 'placeholder': 'e.g., [0.0, 0.1, 0.0]'}),
            'strain_simulation': forms.CheckboxInput(),
            'is_alloy': forms.CheckboxInput(),
            'mole_fraction': forms.NumberInput(attrs={'min': 0, 'max': 1, 'step': 'any', 'required': False, 'placeholder': 'Enter mole fraction (0-1)'}),
        }