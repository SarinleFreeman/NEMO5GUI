# urls.py in your main app directory
from django.contrib import admin
from django.urls import path, include
from .views import home_view, generate_input_deck_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('regions/', include(('regions.urls', 'regions'), namespace='regions')),
    path('materials/', include(('materials.urls', 'materials'), namespace='materials')),
    path('domains/', include(('domains.urls', 'domains'), namespace='domains')),
    path('solver/', include(('solver.urls', 'solver'), namespace='solver')),
    path('boundary/', include(('boundary.urls', 'boundary'), namespace='boundary')),
    path('', home_view, name='home'),
    path('generate-input-deck/', generate_input_deck_view, name='generate_input_deck')
]