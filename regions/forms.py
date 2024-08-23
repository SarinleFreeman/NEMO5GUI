from django import forms
from .models import Region, BoundaryRegion

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'
        widgets = {
            'shape': forms.Select(attrs={'required': True}),
            'tag': forms.TextInput(attrs={
                'required': True, 
                'pattern': '[A-Za-z0-9]+',
                'placeholder': 'Enter a unique alphanumeric tag'
            }),
            'region_number': forms.NumberInput(attrs={
                'min': 1, 
                'required': True,
                'placeholder': 'Enter a unique positive integer'
            }),
            'priority': forms.NumberInput(attrs={
                'min': 1, 
                'required': True,
                'placeholder': 'Enter a unique positive integer'
            }),
            'min_x': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter minimum X coordinate'
            }),
            'max_x': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter maximum X coordinate'
            }),
            'min_y': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter minimum Y coordinate'
            }),
            'max_y': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter maximum Y coordinate'
            }),
            'min_z': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter minimum Z coordinate'
            }),
            'max_z': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter maximum Z coordinate'
            }),
        }

class BoundaryRegionForm(forms.ModelForm):
    rectangles = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter rectangles as: (ID, x, y, width, height), one per line. ID should match region number.',
            'rows': 3
        }),
        required=False
    )

    class Meta:
        model = BoundaryRegion
        fields = '__all__'
        widgets = {
            'shape': forms.Select(attrs={'required': True}),
            'tag': forms.TextInput(attrs={
                'required': True, 
                'pattern': '[A-Za-z0-9]+',
                'placeholder': 'Enter a unique alphanumeric tag for boundary region'
            }),
            'region_number': forms.NumberInput(attrs={
                'min': 1, 
                'required': True,
                'placeholder': 'Enter a unique positive integer for boundary region'
            }),
            'priority': forms.NumberInput(attrs={
                'min': 1, 
                'required': True,
                'placeholder': 'Priority level for the boundary region'
            }),
            'work_plane': forms.Select(attrs={
                'required': True,
                'placeholder': 'Select the work plane (X, Y, Z)'
            }),
            'plane_tolerance': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter plane tolerance'
            }),
            'axis_cut': forms.NumberInput(attrs={
                'required': True,
                'placeholder': 'Enter axis cut number'
            })
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['shape'].initial = '2d'
        self.fields['shape'].disabled = True

        self.fields['rectangles'].initial = "(7,0,-550,600,30)"
        self.fields['rectangles'].label = "(ID/region_number, x, y, width, height)"

    def clean_rectangles(self):
        rectangles_text = self.cleaned_data['rectangles']
        rectangles = []
        for line in rectangles_text.split('\n'):
            line = line.strip()
            if line:
                try:
                    rect = eval(line)
                    if not isinstance(rect, tuple) or len(rect) != 5:
                        raise ValueError
                    rectangles.append(list(rect))
                except:
                    raise forms.ValidationError(f"Invalid rectangle format: {line}")
        return rectangles

    def clean(self):
        cleaned_data = super().clean()
        region_number = cleaned_data.get('region_number')
        rectangles = cleaned_data.get('rectangles')

        if rectangles:
            for rect in rectangles:
                if rect[0] != region_number:
                    raise forms.ValidationError(f"Rectangle ID {rect[0]} does not match region number {region_number}.")

        return cleaned_data