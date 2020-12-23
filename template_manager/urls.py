from django.urls import path
from template_manager.views import (
    manage_templates,TemplateDeleteView,
)

app_name = 'template_manager'


urlpatterns = [
    path('', manage_templates, name='list'),
    path('<int:pk>/delete/', TemplateDeleteView.as_view(), name="remove_template"),
    
]
