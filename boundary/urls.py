from django.urls import path
from . import views

app_name = 'boundary'

urlpatterns = [
    path('', views.BoundaryConditionListView.as_view(), name='boundary_condition_list'),
    path('edit/<int:pk>/', views.BoundaryConditionUpdateView.as_view(), name='edit_boundary_condition'),
    path('delete/<int:pk>/', views.BoundaryConditionDeleteView.as_view(), name='delete_boundary_condition'),
]

