from django.db import OperationalError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from .models import NonlinearPoissonFEM, EMSchrodingerFEM, SemiclassicalFEM
from .forms import NonlinearPoissonFEMForm, EMSchrodingerFEMForm, SemiclassicalFEMForm
import json

class SolverListView(View):
    template_name = 'solvers/solver_list.html'

    def get(self, request):
        context = {}
        domains_exist, regions_exist = self.check_dependencies()
        
        context['dependencies_met'] = domains_exist and regions_exist
        if context['dependencies_met']:
            context['nonlinear_solvers'] = NonlinearPoissonFEM.objects.all()
            context['schrodinger_solvers'] = EMSchrodingerFEM.objects.all()
            context['semiclassical_solvers'] = SemiclassicalFEM.objects.all()
            context['nonlinear_form'] = NonlinearPoissonFEMForm()
            context['schrodinger_form'] = EMSchrodingerFEMForm()
            context['semiclassical_form'] = SemiclassicalFEMForm()
        else:
            if not domains_exist:
                messages.warning(request, "Domains have not been set up yet. Please set up domains before adding solvers.")
            if not regions_exist:
                messages.warning(request, "Regions have not been set up yet. Please set up regions before adding solvers.")

        return render(request, self.template_name, context)

    def post(self, request):
        domains_exist, regions_exist = self.check_dependencies()
        if not (domains_exist and regions_exist):
            messages.error(request, "Error: Both Domains and Regions must be set up before adding solvers.")
            return redirect('solvers:solver_list')

        solver_type = request.POST.get('type')
        if solver_type is None:
            messages.error(request, "Error: Solver type is required.")
            return self.get(request)

        form_classes = {
            'NonlinearPoissonFEM': NonlinearPoissonFEMForm,
            'EMSchrodingerFEM': EMSchrodingerFEMForm,
            'SemiclassicalFEM': SemiclassicalFEMForm
        }

        if solver_type in form_classes:
            form = form_classes[solver_type](request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'{solver_type} added successfully!')
                return redirect('solvers:solver_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            messages.error(request, "Invalid solver type.")

        return self.get(request)

    def check_dependencies(self):
        domains_exist = False
        regions_exist = False
        try:
            from domains.models import Domain
            Domain.objects.first()
            domains_exist = True
        except OperationalError:
            pass

        try:
            from regions.models import Region
            Region.objects.first()
            regions_exist = True
        except OperationalError:
            pass

        return domains_exist, regions_exist

class SolverUpdateView(UpdateView):
    template_name = 'solvers/edit_solver.html'
    success_url = reverse_lazy('solvers:solver_list')

    def get_queryset(self):
        if self.kwargs['type'] == 'nonlinearpoissonfem':
            return NonlinearPoissonFEM.objects.all()
        elif self.kwargs['type'] == 'emschrodingerfem':
            return EMSchrodingerFEM.objects.all()
        elif self.kwargs['type'] == 'semiclassicalfem':
            return SemiclassicalFEM.objects.all()

    def get_form_class(self):
        if self.kwargs['type'] == 'nonlinearpoissonfem':
            return NonlinearPoissonFEMForm
        elif self.kwargs['type'] == 'emschrodingerfem':
            return EMSchrodingerFEMForm
        elif self.kwargs['type'] == 'semiclassicalfem':
            return SemiclassicalFEMForm

class SolverDeleteView(DeleteView):
    template_name = 'solvers/delete_solver.html'
    success_url = reverse_lazy('solvers:solver_list')
    
    # Dictionary to map type keys to their respective models
    model_mapping = {
        'nonlinearpoissonfem': NonlinearPoissonFEM,
        'emschrodingerfem': EMSchrodingerFEM,
        'semiclassicalfem': SemiclassicalFEM
    }
    
    def get_queryset(self):
        # Retrieve the model class based on the type parameter from the URL.
        model = self.model_mapping.get(self.kwargs['type'])
        if not model:
            raise Http404("Solver type not found.")
        return model.objects.all()
    
    def get_object(self, queryset=None):
        # Use the queryset from get_queryset or generate it if not provided
        queryset = queryset or self.get_queryset()
        # Fetch the object by ID using the queryset
        id_ = self.kwargs.get("pk")
        return get_object_or_404(queryset, id=id_)