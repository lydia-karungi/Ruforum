import json
from navutils import MenuMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DetailView,DeleteView, TemplateView, View)

import os
from django.db.models import Q
from contacts.models import User,Student
from .forms import ContactForm,StudentForm,UpdateStudentForm
import tempfile
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from common.choices import COUNTRY_CHOICES, GENDER_CHOICES
from django.contrib.auth.models import Group
from datetime import date
import xlsxwriter
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework import filters


class ContactsListView(LoginRequiredMixin, TemplateView, MenuMixin):
    model = User
    current_menu_item = 'contacts'
    context_object_name = "contact_obj_list"
    template_name = "contacts.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        print(queryset.count())
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)
        context["contact_obj_list"] = self.get_queryset()


        return context



class CreateContactView(LoginRequiredMixin, CreateView):
    model = User
    form_class = ContactForm
    template_name = "create_contact.html"
    success_url = reverse_lazy("contacts:list")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        user = form.save(commit=False)

        user.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:profile'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Contact was created successfully.')
        return super(CreateContactView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CreateContactView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return response

    def get_form_kwargs(self):
        kwargs = super(CreateContactView, self).get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context["user_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class UpdateContactView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ContactForm
    template_name = "create_contact.html"
    success_url = reverse_lazy("contacts:list")

    def form_valid(self, form):
        user = form.save(commit=False)

        user.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:profile'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Contact was updated successfully.')
        return super(UpdateContactView, self).form_valid(form)


    def form_invalid(self, form):
        response = super(UpdateContactView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return response

    def get_form_kwargs(self):
        kwargs = super(UpdateContactView, self).get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context["contact_obj"] = self.object
        context["user_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context

# Contacts Details view
class ContactDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "contact_record"
    template_name = "contact_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)

        context.update({

        })
        return context

# Delete Contact
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'contacts.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
       # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            #if self.request.user != self.object.created_by:
               # raise PermissionDenied
        self.object.delete()
        return redirect("contacts:list")


class StudentsListView(LoginRequiredMixin, TemplateView,MenuMixin):
    model = Student
    current_menu_item = 'students'
    context_object_name = "students"
    template_name = "student_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        graduated_students = self.get_queryset().filter(graduated=True)
        continueing_students = self.get_queryset().filter(graduated=False)
        context["graduated_students"] = graduated_students
        context["continueing_students"] = continueing_students
        context['countries'] = COUNTRY_CHOICES
        context["per_page"] = self.request.POST.get('per_page')
        return context

    

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'export-excel' in request.POST:
            return self.export_excel_report(request, context)
        return self.render_to_response(context)


class CreateStudentView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "create_student.html"
    success_url = reverse_lazy("contacts:students_list")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        student = form.save(commit=False)
        studentgroup= Group.objects.get(name='Students')
        student.user.groups.clear()
        student.user.groups.add(studentgroup)
        student_id = Student.objects.latest('id')
        id = student_id.id
        student.student_no ='RU/'+str(date.today().year)+"/"+format(int(id+1), "06")
        student.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'contacts:students_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Student was created successfully.')
        return redirect('contacts:students_list')

    def form_invalid(self, form):
        response = super(CreateStudentView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return response

    def get_form_kwargs(self):
        kwargs = super(CreateStudentView, self).get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateStudentView, self).get_context_data(**kwargs)
        context["student_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class UpdateStudentView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = UpdateStudentForm
    template_name = "edit_student.html"
    success_url = reverse_lazy("contacts:students_list")

    def post(self, request, *args, **kwargs):
        self.object =self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        student = form.save(commit=False)

        student.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'contacts:students_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Student was updated successfully.')
        return super(UpdateStudentView, self).form_valid(form)


    def form_invalid(self, form):
        response = super(UpdateStudentView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return response

    def get_form_kwargs(self):
        kwargs = super(UpdateStudentView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context["student_obj"] = self.object
        context["student_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context
 #Delete Student
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect('contacts:students_list')

 #graduate student
class GraduateStudentView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.graduated=True
       # grad_date=self.request.GET.get['grad_actual']
        grad_date=self.kwargs['grad_actual']
        self.object.grad_actual = grad_date
        self.object.save()
        return redirect('contacts:students_list')

#Student Details view
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = "student_record"
    template_name = "student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)

        context.update({

        })
        return context

# included them to fetch json data as normal data was slowing down the system
# restframework viewsets 
class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['business_email', 'first_name','last_name','gender','passport_no',
    'country','nationality','job_title','institution','personal_email','mobile','department','=groups__name']

    def get_queryset(self):
        queryset = User.objects.all().order_by('-id')
        
        groups = self.request.query_params.get('groups', None)
        if groups is not None:
            queryset = queryset.filter(group__name=groups)
        return queryset