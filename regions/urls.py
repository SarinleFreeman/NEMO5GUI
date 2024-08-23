from django.urls import path
from .views import RegionListView, RegionUpdateView, RegionDeleteView, BoundaryRegionUpdateView, BoundaryRegionDeleteView

app_name = 'regions'

urlpatterns = [
    path('', RegionListView.as_view(), name='region_list'),
    path('edit/<int:pk>/', RegionUpdateView.as_view(), name='edit_region'),
    path('delete/<int:pk>/', RegionDeleteView.as_view(), name='delete_region'),
    path('edit_boundary/<int:pk>/', BoundaryRegionUpdateView.as_view(), name='edit_boundary_region'),
    path('delete_boundary/<int:pk>/', BoundaryRegionDeleteView.as_view(), name='delete_boundary_region'),
]