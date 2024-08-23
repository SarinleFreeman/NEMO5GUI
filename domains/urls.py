from django.urls import path
from .views import DomainListView, DomainUpdateView, DomainDeleteView

app_name = 'domains'

urlpatterns = [
    path('', DomainListView.as_view(), name='domain_list'),
    path('<int:pk>/edit/', DomainUpdateView.as_view(), name='edit_domain'),
    path('<int:pk>/delete/', DomainDeleteView.as_view(), name='delete_domain'),
]