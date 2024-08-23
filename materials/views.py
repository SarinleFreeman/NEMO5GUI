from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Material
from .forms import MaterialForm
from django.views import View
from django.contrib import messages



class MaterialListView(View):
    template_name = 'materials/material_list.html'

    def get(self, request):
        materials = Material.objects.all()
        form = MaterialForm()  # Instantiate a new form for adding a material
        return render(request, self.template_name, {'materials': materials, 'form': form})
    
    def post(self, request):
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material added successfully!')
            return redirect('materials:material_list')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
        materials = Material.objects.all()
        return render(request, self.template_name, {'materials': materials, 'form': form})
    
    
class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/edit_material.html'
    success_url = reverse_lazy('materials:material_list')

class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'materials/delete_material.html'
    success_url = reverse_lazy('materials:material_list')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Material, id=id_)