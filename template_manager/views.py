from django.shortcuts import render

from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Template
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    CreateView, UpdateView, DetailView,DeleteView, TemplateView, View)


def manage_templates(request):
    
    groups = [
        {'title': 'First Report', 'models': ['grants_reports.FirstReport', 'grants_reports.FirstStudentReport']},
        {'title': 'Middle Reports', 'models': ['grants_reports.Month12Report']},
        {'title': 'Last Report', 'models': ['grants_reports.LastReport']},
       
    ]
    if request.method == "POST":
        TemplateFormSet = modelformset_factory(
            Template, fields=['file'], extra=0)
        for group in groups:
            formset = TemplateFormSet(
                request.POST, request.FILES,
                queryset=Template.objects.filter(model__in=group['models'])
            )
            if formset.is_valid():
                formset.save()
            else:
                print("errors", formset.errors)
        return redirect("template_manager:list")
    else:
        TemplateFormSet = modelformset_factory(
            Template, exclude=[], extra=0,
            widgets={'file': forms.FileInput()})
        formsets = []
        for group in groups:
            formset = TemplateFormSet(
                queryset=Template.objects.filter(model__in=group['models'])
            )
            formsets.append({'title': group['title'], 'formset': formset})
    return render(request, 'templates.html', {'formsets': formsets})



# Delete template
class TemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = Template
    template_name = 'templates.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("template_manager:list")

