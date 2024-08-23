from django.urls import path
from .views import SolverListView, SolverUpdateView, SolverDeleteView

app_name = 'solvers'

urlpatterns = [
    path('', SolverListView.as_view(), name='solver_list'),
    path('edit/<str:type>/<int:pk>/', SolverUpdateView.as_view(), name='edit_solver'),
    path('delete/<str:type>/<int:pk>/', SolverDeleteView.as_view(), name='delete_solver'),
]