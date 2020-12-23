from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)
from .models import ProjectManagement, LogicalFramework
from django.contrib.auth.mixins import LoginRequiredMixin
from navutils import MenuMixin
from .forms import ProjectManagementForm, LogicalFrameworkForm, SelectProjectForm
from django.contrib import messages



#projects list view
class ProjectListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = ProjectManagement
    context_object_name = "project_list"
    template_name = "projectlist.html"
    current_menu_item = 'projects'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        #open_units = self.get_queryset().filter(status='open')
        #close_units = self.get_queryset().filter(status='close')
        context["project_list"] = self.get_queryset().order_by('project_title')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class CreateProjectView(LoginRequiredMixin, CreateView):
    model = ProjectManagement
    form_class = ProjectManagementForm
    template_name = "create_project.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateProjectView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save project
        projectobject = form.save(commit=False)

        projectobject.created_by = self.request.user

        projectobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'project_management:projectlist'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Project was created successfully.')
        return redirect("project_management:projectlist")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context["project_form"] = context["form"]

        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = ProjectManagement
    context_object_name = "projectrecord"
    template_name = "view_project.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        unitrecord = context["projectrecord"]
        return context

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectManagement
    form_class = ProjectManagementForm
    template_name = "create_project.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ProjectUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Unit
        unitobject = form.save(commit=False)
        unitobject.save()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'project_management:projectlist'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Project updated successfully.')
        return redirect("project_management:projectlist")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context["projectobj"] = self.object
        context["project_form"] = context["form"]
        return context

#Delete project
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectManagement
    template_name = 'view_project.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("project_management:projectlist")

class SelectProjectView(LoginRequiredMixin, CreateView):
    model = ProjectManagement
    form_class = SelectProjectForm
    template_name = "select_project.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)

        return self.form_invalid(form, self.other_form)

    def form_valid(self, form):

        call = form.cleaned_data['call']


    def form_invalid(self, form, other_form):
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(SelectProjectView, self).get_context_data(**kwargs)
        print("context", context, "kwargs", kwargs)
        return context

class ProjectaActivitiesListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = LogicalFramework
    context_object_name = "activities_list"
    template_name = "activitieslist.html"
    current_menu_item = 'projects'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectaActivitiesListView, self).get_context_data(**kwargs)

        #open_units = self.get_queryset().filter(status='open')
        #close_units = self.get_queryset().filter(status='close')
        context["activities_list"] = self.get_queryset().order_by('project__project_title')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

#create framework view
class CreateFrameworkView(LoginRequiredMixin, CreateView):
    model = LogicalFramework
    form_class = LogicalFrameworkForm
    template_name = "create_project_framework.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateFrameworkView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFrameworkView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save project
        projectobject = form.save(commit=False)

        projectobject.created_by = self.request.user

        projectobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'project_management:activitieslist'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Project Framework was created successfully.')
        return redirect("project_management:activitieslist")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFrameworkView, self).get_context_data(**kwargs)
        context["project_form"] = context["form"]

        return context

class FrameworkDetailView(LoginRequiredMixin, DetailView):
    model = LogicalFramework
    context_object_name = "projectrecord"
    template_name = "view_framework.html"

    def get_context_data(self, **kwargs):
        context = super(FrameworkDetailView, self).get_context_data(**kwargs)
        unitrecord = context["projectrecord"]
        return context

class FrameworkUpdateView(LoginRequiredMixin, UpdateView):
    model = LogicalFramework
    form_class = LogicalFrameworkForm
    template_name = "create_project_framework.html"

    def dispatch(self, request, *args, **kwargs):
        return super(FrameworkUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FrameworkUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Unit
        unitobject = form.save(commit=False)
        unitobject.save()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'project_management:activitieslist'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Project updated successfully.')
        return redirect("project_management:activitieslist")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FrameworkUpdateView, self).get_context_data(**kwargs)
        context["projectobj"] = self.object
        context["project_form"] = context["form"]
        return context

class FrameworkDeleteView(LoginRequiredMixin, DeleteView):
    model = LogicalFramework
    template_name = 'view_framework.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("project_management:activitieslist")
