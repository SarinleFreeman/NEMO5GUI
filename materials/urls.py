from django.urls import path
from .views import MaterialDeleteView, MaterialListView, MaterialUpdateView

app_name = 'materials'

urlpatterns = [
    path('', MaterialListView.as_view(), name='material_list'),
    path('<int:pk>/edit/', MaterialUpdateView.as_view(), name='edit_material'),
    path('<int:pk>/delete/', MaterialDeleteView.as_view(), name='delete_material'),
]