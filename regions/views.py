from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .models import Region, BoundaryRegion
from .forms import RegionForm, BoundaryRegionForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages

class RegionListView(View):
    template_name = 'regions/region_list.html'

    def get(self, request):
        regions = Region.objects.all()
        boundary_regions = BoundaryRegion.objects.all()
        region_form = RegionForm()
        boundary_region_form = BoundaryRegionForm()
        print(f"Regions: {regions.count()}, Boundary Regions: {boundary_regions.count()}")

        return render(request, self.template_name, {
            'regions': regions, 
            'boundary_regions': boundary_regions,
            'region_form': region_form,
            'boundary_region_form': boundary_region_form
        })

    def post(self, request):
        if 'submit_region' in request.POST:
            form = RegionForm(request.POST)
            model_type = 'Region'
        elif 'submit_boundary_region' in request.POST:
            form = BoundaryRegionForm(request.POST)
            model_type = 'Boundary Region'

        if form.is_valid():
            form.save()
            messages.success(request, f'{model_type} added successfully!')
            return redirect('regions:region_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            return self.get(request)

class RegionUpdateView(UpdateView):
    model = Region
    form_class = RegionForm
    template_name = 'regions/edit_region.html'
    success_url = reverse_lazy('regions:region_list')

class BoundaryRegionUpdateView(UpdateView):
    model = BoundaryRegion
    form_class = BoundaryRegionForm
    template_name = 'regions/edit_region.html'
    success_url = reverse_lazy('regions:region_list')

class RegionDeleteView(DeleteView):
    model = Region
    template_name = 'regions/delete_region.html'
    success_url = reverse_lazy('regions:region_list')

class BoundaryRegionDeleteView(DeleteView):
    model = BoundaryRegion
    template_name = 'regions/delete_region.html'
    success_url = reverse_lazy('regions:region_list')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        if 'region' in self.request.path:
            return get_object_or_404(Region, id=id_)
        elif 'boundary_region' in self.request.path:
            return get_object_or_404(BoundaryRegion, id=id_)