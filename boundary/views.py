from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .models import BoundaryCondition
from .forms import BoundaryConditionForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages

class BoundaryConditionListView(View):
    template_name = 'boundary/boundary_condition_list.html'

    def get(self, request):
        boundary_conditions = BoundaryCondition.objects.all()
        form = BoundaryConditionForm()
        print(f"Boundary Conditions: {boundary_conditions.count()}")

        return render(request, self.template_name, {
            'boundary_conditions': boundary_conditions,
            'form': form
        })

    def post(self, request):
        form = BoundaryConditionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Boundary Condition added successfully!')
            return redirect('boundary:boundary_condition_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            return self.get(request)


class BoundaryConditionUpdateView(UpdateView):
    model = BoundaryCondition
    form_class = BoundaryConditionForm
    template_name = 'boundary/edit_boundary_condition.html'
    success_url = reverse_lazy('boundary:boundary_condition_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    
class BoundaryConditionDeleteView(DeleteView):
    model = BoundaryCondition
    template_name = 'boundary/delete_boundary_condition.html'
    success_url = reverse_lazy('boundary:boundary_condition_list')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(BoundaryCondition, id=id_)