from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Domain
from .forms import DomainForm
from django.views import View
from django.contrib import messages

class DomainListView(View):
    """
    A view to display a list of domains and a form for adding a new domain.
    """
    template_name = 'domains/domain_list.html'

    def get(self, request):
        domains = Domain.objects.all()
        form = DomainForm()  # Instantiate a new form for adding a domain
        return render(request, self.template_name, {'domains': domains, 'form': form})

    def post(self, request):
        form = DomainForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Domain added successfully!')
            return redirect('domains:domain_list')
        else:
            messages.error(request, 'Error while adding the domain.')
        domains = Domain.objects.all()
        return render(request, self.template_name, {'domains': domains, 'form': form})

class DomainUpdateView(UpdateView):
    """
    A view that handles updating an existing domain.
    """
    model = Domain
    form_class = DomainForm
    template_name = 'domains/edit_domain.html'
    success_url = reverse_lazy('domains:domain_list')

class DomainDeleteView(DeleteView):
    """
    A view that handles the deletion of a domain.
    """
    model = Domain
    template_name = 'domains/delete_domain.html'
    success_url = reverse_lazy('domains:domain_list')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Domain, id=id_)