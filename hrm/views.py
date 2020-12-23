from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)

# from hrm.forms import DepartmentForm, DepartmentCommentForm, \
#    DepartmentAttachmentForm, EmailForm
from common.models import Attachments
from hrm.models import (
    Department, StaffProfile, StaffTravel, AssetCategory, Asset,LeaveType,
    Vehicle, Contract, LeaveAssignment,LeaveApplication,Leave,Month6Appraisal
)
from django.contrib import messages
from contacts.models import User
from .models import BaseStaffRequest
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .forms import (
    DepartmentForm, StaffProfileAdminCreateForm,StaffProfileEditForm,
    StaffTravelForm, AssetCategoryForm, AssetForm,LeaveTypeForm,
    VehicleForm, AssignAssetForm, ContractForm, DependantsForm, DependantsFormSet, AlevelBackgroundFormSet,
    TravelAttachmentForm,LeaveAssignmentForm, LeaveApplicationForm,LeaveHRConfirmationForm,
    LeaveSupervisorRecommendationForm,LeaveAppApprovalForm,EditLeaveAssignmentForm,
    Month6AppraisalForm,Month6AppraisalActivityFormSet,Month6PlannedAppraisalActivityFormSet
)
from navutils import MenuMixin
from .serializers import (LeaveSerializer,LeaveAssignmentSerializer,LeaveApplicationsSerializer,ApprovedLeaveSerializer,
Month6AppraisalSerializer)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from datetime import datetime


class DepartmentsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Department
    context_object_name = "deparemnt_list"
    template_name = "departments.html"
    current_menu_item = 'deparments'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    Q(name__icontains=request_post.get('name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(DepartmentsListView, self).get_context_data(**kwargs)
        context["departments"] = self.get_queryset().order_by('name')

        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('applicant_name') or self.request.POST.get('status') or
                self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('tab_status'):
            tab_status = self.request.POST.get('tab_status')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# class CreateDepartmentView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateDepartmentView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "create_department.html"

    def dispatch(self, request, *args, **kwargs):

        # self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateDepartmentView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateDepartmentView, self).get_form_kwargs()
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
        # Save Department
        departmentobject = form.save(commit=False)

        departmentobject.created_by = self.request.user

        departmentobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_department")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:department_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Creaded New Department successfully.')
        return redirect("hrm:department_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateDepartmentView, self).get_context_data(**kwargs)
        context["department_form"] = context["form"]

        return context


# SalesAccessRequiredMixin,
class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = "departmentrecord"
    template_name = "view_department.html"

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)
        departmentrecord = context["departmentrecord"]
        return context


# SalesAccessRequiredMixin,
class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "create_department.html"

    def dispatch(self, request, *args, **kwargs):
        return super(DepartmentUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(DepartmentUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Department
        departmentobject = form.save(commit=False)
        departmentobject.save()
        # departmentobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:department_list'), 'error': False}
            return JsonResponse(data)
            messages.add_message(self.request, messages.SUCCESS, 'Department updated successfully.')
        return redirect("hrm:department_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(DepartmentUpdateView, self).get_context_data(**kwargs)
        context["departmentobj"] = self.object
        context["departmentform"] = context["form"]
        return context


# SalesAccessRequiredMixin,
class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'view_department.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:department_list")


class StaffProfilesListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = StaffProfile
    context_object_name = "staff_list"
    template_name = "staff.html"
    current_menu_item = 'deparments'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('Staff_ID'):
                queryset = queryset.filter(
                    Q(id_number__icontains=request_post.get('Staff_ID')))
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('first_name')))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    Q(user__last_name__icontains=request_post.get('last_name')))
            if request_post.get('department'):
                queryset = queryset.filter(
                    Q(department__name__icontains=request_post.get('department')))
            if request_post.get('position'):
                queryset = queryset.filter(
                    Q(role__name__icontains=request_post.get('position')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(StaffProfilesListView, self).get_context_data(**kwargs)
        context["staff_list"] = self.get_queryset().order_by('user__first_name', 'user__last_name')

        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateStaffProfileView(LoginRequiredMixin, CreateView):
    model = StaffProfile
    form_class = StaffProfileAdminCreateForm
    template_name = "create_staff.html"

    def dispatch(self, request, *args, **kwargs):

        # self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateStaffProfileView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateStaffProfileView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        self.dependants = DependantsFormSet(request.POST, prefix='dependant_set')
        self.alevel = AlevelBackgroundFormSet(request.POST, prefix='education_set')
        form = self.get_form()
        formsets_valid = (
                    self.dependants.is_valid(),
                    self.alevel.is_valid(),
            )
        if form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save StaffProfile
        staff_profileobject = form.save(commit=False)
        staff_profileobject.created_by = self.request.user
        staff_profileobject.save()
        self.dependants.instance = staff_profileobject
        self.dependants.save()
        self.alevel.instance = staff_profileobject
        self.alevel.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:staff_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Staff Profile Submitted successfully.')
        return redirect("hrm:staff_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form, dependants=self.dependants, alevel=self.alevel),

        )
 
    def get_context_data(self, **kwargs):
        context = super(CreateStaffProfileView, self).get_context_data(**kwargs)
        context["staff_profile_form"] = context["form"]
        context["dependant_form_set"] = context.get('dependants') or DependantsFormSet(prefix="dependant_set")
        context["Alevel_form_set"] = context.get('alevel') or AlevelBackgroundFormSet(prefix="education_set")

        return context


# SalesAccessRequiredMixin,
class StaffProfileDetailView(LoginRequiredMixin, DetailView):
    model = StaffProfile
    context_object_name = "staff_profilerecord"
    template_name = "view_staff.html"

    def get_context_data(self, **kwargs):
        context = super(StaffProfileDetailView, self).get_context_data(**kwargs)
        staff_profilerecord = context["staff_profilerecord"]
        return context


# SalesAccessRequiredMixin,
class StaffProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = StaffProfile
    form_class = StaffProfileEditForm
    template_name = "create_staff.html"

    def dispatch(self, request, *args, **kwargs):
        return super(StaffProfileUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StaffProfileUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.dependants = DependantsFormSet(request.POST, prefix='dependant_set', instance=self.object)
        self.alevel = AlevelBackgroundFormSet(request.POST, prefix='education_set', instance=self.object)
        form = self.get_form()
        formsets_valid = (
                    self.dependants.is_valid(),
                    self.alevel.is_valid(),
            )
        if form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            
        return self.form_invalid(form)

    def form_valid(self, form):
         # Save StaffProfile
        staff_profileobject = form.save(commit=False)
        staff_profileobject.created_by = self.request.user
        staff_profileobject.save()
        self.dependants.instance = staff_profileobject
        self.dependants.save()
        self.alevel.instance = staff_profileobject
        self.alevel.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:staff_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Staff Profile Updated successfully.')
        return redirect("hrm:staff_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(StaffProfileUpdateView, self).get_context_data(**kwargs)
        context["staff_profileobj"] = self.object
        context["staff_profileform"] = context["form"]
        context["dependant_form_set"] = context.get('dependants') or DependantsFormSet(prefix="dependant_set", instance=self.object)
        context["Alevel_form_set"] = context.get('alevel') or AlevelBackgroundFormSet(prefix="education_set", instance=self.object)
        return context


class StaffProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = StaffProfile
    template_name = 'view_staff.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:staff_list")


class StaffTravelsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = StaffTravel
    context_object_name = "travel_list"
    template_name = "travels.html"
    current_menu_item = 'travels'

    def get_queryset(self):
        queryset = self.model.objects.order_by('-id')
        request_post = self.request.POST
        if request_post:
            if request_post.get('place'):
                queryset = queryset.filter(
                    Q(place_of_visit__icontains=request_post.get('place')))

            if request_post.get('start_date'):
                queryset = queryset.filter(
                    Q(start_date__icontains=request_post.get('start_date')))
            if request_post.get('end_date'):
                queryset = queryset.filter(
                    Q(end_date__icontains=request_post.get('end_date')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(StaffTravelsListView, self).get_context_data(**kwargs)
        context["travels"] = self.get_queryset().order_by('-start_date')
        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('applicant_name') or self.request.POST.get('status') or
                self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('tab_status'):
            tab_status = self.request.POST.get('tab_status')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateStaffTravelView(LoginRequiredMixin, CreateView):
    model = StaffTravel
    form_class = StaffTravelForm
    template_name = "create_travel.html"

    def dispatch(self, request, *args, **kwargs):

        # self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateStaffTravelView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateStaffTravelView, self).get_form_kwargs()
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
        # Save StaffTravel
        travelobject = form.save(commit=False)
        travelobject.created_by = self.request.user
        travelobject.save()
        form.save_m2m()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_travel")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:travel_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Staff Travel Submitted successfully.')
        return redirect("hrm:travel_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateStaffTravelView, self).get_context_data(**kwargs)
        context["travel_form"] = context["form"]

        return context


# SalesAccessRequiredMixin,
class StaffTravelDetailView(LoginRequiredMixin, DetailView):
    model = StaffTravel
    context_object_name = "travelrecord"
    template_name = "view_travel.html"

    def get_context_data(self, **kwargs):
        context = super(StaffTravelDetailView, self).get_context_data(**kwargs)
        travelrecord = context["travelrecord"]
        context['attachments'] = travelrecord.travel_attachment.all()
        return context


# SalesAccessRequiredMixin,
class StaffTravelUpdateView(LoginRequiredMixin, UpdateView):
    model = StaffTravel
    form_class = StaffTravelForm
    template_name = "create_travel.html"

    def dispatch(self, request, *args, **kwargs):
        return super(StaffTravelUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StaffTravelUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save StaffTravel
        travelobject = form.save(commit=False)
        travelobject.save()
        form.save_m2m()
        # travelobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:travel_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Staff Travel Submitted successfully.')
        return redirect("hrm:travel_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(StaffTravelUpdateView, self).get_context_data(**kwargs)
        context["travelobj"] = self.object
        context["travelform"] = context["form"]
        return context


# SalesAccessRequiredMixin,
class StaffTravelDeleteView(LoginRequiredMixin, DeleteView):
    model = StaffTravel
    template_name = 'view_travel.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:travel_list")


class AssetCategorysListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = AssetCategory
    context_object_name = "deparemnt_list"
    template_name = "asset_categories.html"
    current_menu_item = 'deparments'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('asset_category_name'):
                queryset = queryset.filter(
                    Q(name__icontains=request_post.get('asset_category_name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssetCategorysListView, self).get_context_data(**kwargs)
        context["asset_categories"] = self.get_queryset().order_by('name')
        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('applicant_name') or self.request.POST.get('status') or
                self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('tab_status'):
            tab_status = self.request.POST.get('tab_status')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# asset categories
class CreateAssetCategoryView(LoginRequiredMixin, CreateView):
    model = AssetCategory
    form_class = AssetCategoryForm
    template_name = "create_asset_category.html"

    def dispatch(self, request, *args, **kwargs):

        return super(
            CreateAssetCategoryView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateAssetCategoryView, self).get_form_kwargs()
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
        # Save AssetCategory
        asset_categoryobject = form.save(commit=False)

        asset_categoryobject.created_by = self.request.user

        asset_categoryobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_asset_category")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:asset_category_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Asset Category Submitted successfully.')
        return redirect("hrm:asset_category_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateAssetCategoryView, self).get_context_data(**kwargs)
        context["asset_category_form"] = context["form"]

        return context


# SalesAccessRequiredMixin,
class AssetCategoryDetailView(LoginRequiredMixin, DetailView):
    model = AssetCategory
    context_object_name = "asset_categoryrecord"
    template_name = "view_asset_category.html"

    def get_context_data(self, **kwargs):
        context = super(AssetCategoryDetailView, self).get_context_data(**kwargs)
        asset_categoryrecord = context["asset_categoryrecord"]
        return context


# SalesAccessRequiredMixin,
class AssetCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = AssetCategory
    form_class = AssetCategoryForm
    template_name = "create_asset_category.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssetCategoryUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssetCategoryUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save AssetCategory
        asset_categoryobject = form.save(commit=False)
        asset_categoryobject.save()
        # asset_categoryobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:asset_category_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Asset Category updated successfully.')
        return redirect("hrm:asset_category_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(AssetCategoryUpdateView, self).get_context_data(**kwargs)
        context["asset_categoryobj"] = self.object
        context["asset_categoryform"] = context["form"]
        return context


# SalesAccessRequiredMixin,
class AssetCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = AssetCategory
    template_name = 'view_asset_category.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:asset_category_list")


class AssetsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Asset
    form_class = AssignAssetForm
    context_object_name = "deparemnt_list"
    template_name = "assets.html"
    current_menu_item = 'assets'

    def get_queryset(self):
        queryset = self.model.objects.order_by('-Id')
        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    Q(name__icontains=request_post.get('name')))
            if request_post.get('serial'):
                queryset = queryset.filter(
                    Q(serial_number__icontains=request_post.get('serial')))
            if request_post.get('manufacturer'):
                queryset = queryset.filter(
                    Q(manufacturer__icontains=request_post.get('manufacturer')))

            if request_post.get('assigned'):
                queryset = queryset.filter(
                    Q(assigned_to__user__first_name__icontains=request_post.get('assigned')) |
                    Q(assigned_to__user__last_name__icontains=request_post.get('assigned'))
                )
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssetsListView, self).get_context_data(**kwargs)

        context["assets"] = self.get_queryset().order_by('name')
        context["form"] = AssignAssetForm

        context["per_page"] = self.request.POST.get('per_page')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# class CreateAssetView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateAssetView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "create_asset.html"

    def dispatch(self, request, *args, **kwargs):

        # self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateAssetView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateAssetView, self).get_form_kwargs()
        # kwargs.update({"asset": True})
        # kwargs.update({"request_user": self.request.user})
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     kwargs.update({"request_user": self.request.user})
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
        # Save Asset
        assetobject = form.save(commit=False)

        assetobject.created_by = self.request.user

        assetobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_asset")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:asset_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Asset Submitted successfully.')
        return redirect("hrm:asset_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateAssetView, self).get_context_data(**kwargs)
        context["asset_form"] = context["form"]

        return context


# SalesAccessRequiredMixin,
class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    context_object_name = "assetrecord"
    template_name = "view_asset.html"

    def get_context_data(self, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)
        assetrecord = context["assetrecord"]
        return context


# SalesAccessRequiredMixin,
class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "create_asset.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssetUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssetUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Asset
        assetobject = form.save(commit=False)
        assetobject.save()
        # assetobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:asset_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Asset updated successfully.')
        return redirect("hrm:asset_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(AssetUpdateView, self).get_context_data(**kwargs)
        context["assetobj"] = self.object
        context["assetform"] = context["form"]
        return context


# SalesAccessRequiredMixin,
class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'view_asset.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:asset_list")


class LeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = LeaveType.objects.all().order_by('-id')
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = '__all__'



class LeavesListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = LeaveType
    context_object_name = "leave_list"
    template_name = "leaves.html"
    current_menu_item = 'leaves'

    def get_queryset(self):
        queryset = self.model.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeavesListView, self).get_context_data(**kwargs)

        context["leaves"] = self.get_queryset().order_by('-leave_name')
        context["states"] = BaseStaffRequest.STATUS_CHOICES
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# class CreateLeaveView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateLeaveView(LoginRequiredMixin, CreateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = "create_leave.html"

    def dispatch(self, request, *args, **kwargs):

        # self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateLeaveView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateLeaveView, self).get_form_kwargs()
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
        # Save Leave
        leaveobject = form.save(commit=False)

        leaveobject.created_by = self.request.user

        leaveobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_leave")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Type Submitted successfully.')
        return redirect("hrm:leave_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateLeaveView, self).get_context_data(**kwargs)
        context["leave_form"] = context["form"]

        return context



# SalesAccessRequiredMixin,
class LeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = "create_leave.html"

    def dispatch(self, request, *args, **kwargs):
        return super(LeaveUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LeaveUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Leave
        leaveobject = form.save(commit=False)
        leaveobject.save()
        # leaveobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Staff Leave updated successfully.')
        return redirect("hrm:leave_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(LeaveUpdateView, self).get_context_data(**kwargs)
        context["leaveobj"] = self.object
        context["leaveform"] = context["form"]
        return context


# SalesAccessRequiredMixin,
class LeaveDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaveType
    template_name = 'view_leave.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:leave_list")

# leave assignment view
class CreateLeaveAssignmentView(LoginRequiredMixin, CreateView):
    model = LeaveAssignment
    form_class = LeaveAssignmentForm
    template_name = "create_leave_assignment.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateLeaveAssignmentView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateLeaveAssignmentView, self).get_form_kwargs()
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
        # Save Leave
        staffs = self.request.POST.getlist('staff')
        leaveassignments_list=[]
        leave_type_id = self.request.POST.get('leave_type')
        leave_type_instance = LeaveType.objects.get(id=leave_type_id)
        start_date = self.request.POST.get('start_date')
        leave_days = self.request.POST.get('leave_days')
        year = self.request.POST.get('year')
        print(leave_type_id)
        for staff in staffs:
            leaveassigmentstaff = StaffProfile.objects.get(id=staff)
            leaveobject = LeaveAssignment(leave_type=leave_type_instance,year=year,start_date=start_date,staff=leaveassigmentstaff, leave_days=leave_days)
            leaveassignments_list.append(leaveobject)
        LeaveAssignment.objects.bulk_create(leaveassignments_list)
        #print(leaveassignments_list)
        
        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_leave")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Type Submitted successfully.')
        return redirect("hrm:leave_assignments")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateLeaveAssignmentView, self).get_context_data(**kwargs)
        context["leave_form"] = context["form"]
        context['staffs'] = StaffProfile.objects.all()

        return context


# leave assignment view
class EditLeaveAssignmentView(LoginRequiredMixin, UpdateView):
    model = LeaveAssignment
    form_class = EditLeaveAssignmentForm
    template_name = "edit_leave_assignment.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            EditLeaveAssignmentView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditLeaveAssignmentView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Leave
        leaveobject = form.save(commit=False)

        leaveobject.created_by = self.request.user

        leaveobject.save()
        form.save_m2m()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_leave")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Assignment updated successfully.')
        return redirect("hrm:leave_assignments")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(EditLeaveAssignmentView, self).get_context_data(**kwargs)
        context["leave_form"] = context["form"]

        return context

class VehiclesListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Vehicle
    context_object_name = "vehicle_list"
    template_name = "vehicles.html"
    current_menu_item = 'vehicles'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('vehicle_name'):
                queryset = queryset.filter(
                    Q(registration_plate__icontains=request_post.get('vehicle_name')))
            if request_post.get('model'):
                queryset = queryset.filter(
                    Q(vehicle_model__icontains=request_post.get('model')))
            if request_post.get('make'):
                queryset = queryset.filter(
                    Q(make__icontains=request_post.get('make')))
            if request_post.get('staff'):
                queryset = queryset.filter(
                    Q(assigned_to__user__first_name__icontains=request_post.get('staff')) |
                    Q(assigned_to__user__last_name__icontains=request_post.get('staff')))

            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(VehiclesListView, self).get_context_data(**kwargs)
        context["vehicles"] = self.get_queryset().order_by('registration_plate')
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# class CreateVehicleView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateVehicleView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "create_vehicle.html"

    def dispatch(self, request, *args, **kwargs):

        return super(
            CreateVehicleView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateVehicleView, self).get_form_kwargs()
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
        # Save Vehicle
        vehicleobject = form.save(commit=False)

        vehicleobject.created_by = self.request.user

        vehicleobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("hrm:new_vehicle")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:vehicle_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Vehicle record Submitted successfully.')
        return redirect("hrm:vehicle_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateVehicleView, self).get_context_data(**kwargs)
        context["vehicle_form"] = context["form"]

        return context


# SalesAccessRequiredMixin,
class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    context_object_name = "vehiclerecord"
    template_name = "view_vehicle.html"

    def get_context_data(self, **kwargs):
        context = super(VehicleDetailView, self).get_context_data(**kwargs)
        vehiclerecord = context["vehiclerecord"]
        return context


# SalesAccessRequiredMixin,
class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "create_vehicle.html"

    def dispatch(self, request, *args, **kwargs):
        return super(VehicleUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(VehicleUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Vehicle
        vehicleobject = form.save(commit=False)
        vehicleobject.save()
        # vehicleobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:vehicle_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Vehicle details updated successfully.')
        return redirect("hrm:vehicle_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(VehicleUpdateView, self).get_context_data(**kwargs)
        context["vehicleobj"] = self.object
        context["vehicleform"] = context["form"]
        return context


# vehicle delete view
class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'view_vehicle.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.delete()
        return redirect("hrm:vehicle_list")


class CalendarView(MenuMixin, LoginRequiredMixin, TemplateView):
    template_name = "calendar.html"
    current_menu_item = 'calendar'

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class AssignAssetView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssignAssetForm
    template_name = "assets.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssignAssetView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssignAssetView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Grantapplication
        assetobject = form.save(commit=False)
        assetobject.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:asset_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Asset Assigned staff successfully.')
        return redirect("hrm:asset_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(AssignAssetView, self).get_context_data(**kwargs)
        context["assetObject"] = self.object
        context["asset_form"] = context["form"]
        return context


# contract list view
class ContractListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Contract
    context_object_name = "contract_list"
    template_name = "contracts.html"
    current_menu_item = 'contracts'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('contract_name'):
                queryset = queryset.filter(
                    Q(contract_name__icontains=request_post.get('contract_name')))
            if request_post.get('status'):
                queryset = queryset.filter(
                    contract_status__icontains=request_post.get('status'))
            if request_post.get('type'):
                queryset = queryset.filter(
                    contract_type__icontains=request_post.get('type'))
            if request_post.get('funder'):
                queryset = queryset.filter(
                    Q(funder__icontains=request_post.get('funder')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ContractListView, self).get_context_data(**kwargs)
        context["contracts"] = self.get_queryset().order_by('-start_date')
        context["per_page"] = self.request.POST.get('per_page')

        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('applicant_name') or self.request.POST.get('status') or
                self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('tab_status'):
            tab_status = self.request.POST.get('tab_status')
        context['tab_status'] = tab_status
        context['contract_types'] = Contract.CONTRACT_TYPE
        context['states'] = Contract.CONTRACT_STATUS
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# create contacts
class CreateContractView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "create_contract.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateContractView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateContractView, self).get_form_kwargs()
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
        # Save contract
        contractobject = form.save(commit=False)
        contractobject.created_by = self.request.user
        contractobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:contract_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Contract record Submitted successfully.')
        return redirect("hrm:contract_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateContractView, self).get_context_data(**kwargs)
        context["contract_form"] = context["form"]

        return context


# contract details
class ContractDetailView(LoginRequiredMixin, DetailView):
    model = Contract
    context_object_name = "contractrecord"
    template_name = "view_contract.html"

    def get_context_data(self, **kwargs):
        context = super(ContractDetailView, self).get_context_data(**kwargs)
        contractrecord = context["contractrecord"]
        return context


# update contact
class ContractUpdateView(LoginRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "create_contract.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ContractUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ContractUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save contract
        contractobject = form.save(commit=False)
        contractobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:contract_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Contract details updated successfully.')
        return redirect("hrm:contract_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ContractUpdateView, self).get_context_data(**kwargs)
        context["contractobj"] = self.object
        context["contract_form"] = context["form"]
        return context


# contract delete view
class ContractDeleteView(LoginRequiredMixin, DeleteView):
    model = Contract
    template_name = 'view_contract.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("hrm:contract_list")


# attach document to staff travel
class AddAttachmentView(LoginRequiredMixin, CreateView):
    model = Attachments
    form_class = TravelAttachmentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.travel = get_object_or_404(StaffTravel, id=request.POST.get('travel_id'))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

        data = {
            'error': "You don't have permission to add attachment \
            for this account."}
        return JsonResponse(data)

    def form_valid(self, form):
        attachment = form.save(commit=False)
        attachment.created_by = self.request.user
        attachment.file_name = attachment.attachment.name
        attachment.travel = self.travel
        attachment.save()
        return JsonResponse({
            "attachment_id": attachment.id,
            "attachment": attachment.file_name,
            "attachment_url": attachment.attachment.url,
            "download_url": reverse('common:download_attachment',
                                    kwargs={'pk': attachment.id}),
            "attachment_display": attachment.get_file_type_display(),
            "created_on": attachment.created_on,
            "created_by": attachment.created_by.business_email,
            "file_type": attachment.file_type()
        })

    def form_invalid(self, form):
        print(form.errors)
        return JsonResponse({"error": form['attachment'].errors})



class LeaveAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leaves to be assigned to staffs.
    """
    queryset = LeaveAssignment.objects.all().order_by('-id')
    serializer_class = LeaveAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields =['leave_type__leave_name','staff__first_name','staff__last_name','start_date','leave_days','year']



class LeavesAssignmentListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = LeaveAssignment
    template_name = "leave_assignemts.html"
    current_menu_item = 'leaves'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeavesAssignmentListView, self).get_context_data(**kwargs)
        context["assignments"] = self.get_queryset().order_by('-id')
        return context

# create Leave application view
class CreateLeaveApplicationView(LoginRequiredMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = "create_leave_application.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateLeaveApplicationView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateLeaveApplicationView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        # Save leave application
        leaveobject = form.save(commit=False)
        staff = StaffProfile.objects.get(user=self.request.user)
        leaveobject.staff = staff
        leaveobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_applications'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Application Submitted successfully.')
        return redirect("hrm:leave_applications")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateLeaveApplicationView, self).get_context_data(**kwargs)

        return context

# Edit leave application
class EditLeaveApplicationView(LoginRequiredMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = "create_leave_application.html"

    def dispatch(self, request, *args, **kwargs):
        return super(EditLeaveApplicationView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditLeaveApplicationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save leave application
        leaveobject = form.save(commit=False)
        staff = StaffProfile.objects.get(user=self.request.user)
        leaveobject.staff = staff
        leaveobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_applications'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Application Submitted successfully.')
        return redirect("hrm:leave_applications")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(EditLeaveApplicationView, self).get_context_data(**kwargs)

        return context

class LeaveApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leave applications.
    """
    #queryset = LeaveApplication.objects.all().order_by('-id')
    serializer_class = LeaveApplicationsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields =['leave_assignment__leave_type__leave_name','staff__first_name','staff__last_name','from_date','end_date','leave_days_requested','contact_person','approval']

    def get_queryset(self):
        """
        This view should return a list of all the leave applications
        for the currently authenticated user.
        """
        user = self.request.user
        queries= LeaveApplication.objects.all().order_by('-id')

        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administrative/HR').exists():
            queryset = queries
        else:
            staff = StaffProfile.objects.get(user=user)
            queryset = queries.filter(staff__in=staff)

        return queryset
class LeavesApplicationListView(MenuMixin, LoginRequiredMixin, TemplateView):
    template_name = "leave_applications.html"
    current_menu_item = 'leaves'

# Leave HR Comment
class LeaveApplicationHRCommentView(LoginRequiredMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveHRConfirmationForm
    template_name = "leave_hrcomment.html"

    
    def dispatch(self, request, *args, **kwargs):
        return super(LeaveApplicationHRCommentView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LeaveApplicationHRCommentView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save leave application
        leaveobject = form.save(commit=False)
        leaveobject.human_resource_officer = self.request.user
        leaveobject.hr_comment_date = datetime.now()
        leaveobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_applications'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Comment Submitted successfully.')
        return redirect("hrm:leave_applications")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(LeaveApplicationHRCommentView, self).get_context_data(**kwargs)
        context['leave']= self.get_object()

        return context

# comment by supervisor
class LeaveSupervisorRecommendationView(LoginRequiredMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveSupervisorRecommendationForm
    template_name = "leave_supervisorreco.html"

    
    def dispatch(self, request, *args, **kwargs):
        return super(LeaveSupervisorRecommendationView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LeaveSupervisorRecommendationView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save leave application
        leaveobject = form.save(commit=False)
        supervisor = StaffProfile.objects.get(user=self.request.user)
        leaveobject.supervisor = supervisor
        leaveobject.recommendation_date = datetime.now()
        leaveobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_applications'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Comment Submitted successfully.')
        return redirect("hrm:leave_applications")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(LeaveSupervisorRecommendationView, self).get_context_data(**kwargs)
        context['leave']= self.get_object()

        return context

# approve leave application
class ApproveLeaveApplicationView(LoginRequiredMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveAppApprovalForm
    template_name = "view_leave_application.html"

    
    def dispatch(self, request, *args, **kwargs):
        return super(ApproveLeaveApplicationView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ApproveLeaveApplicationView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save leave application
        leaveapplication = form.save(commit=False)
        leaveapplication.approval = form.cleaned_data.get('approval')
        leaveapplication.date_approved =  datetime.now()
        leaveapplication.approved_by = self.request.user
        leaveapplication.save()
        leave_application = self.get_object()
        start = form.cleaned_data.get('start')
        end = form.cleaned_data.get('end')
        leave_days = form.cleaned_data.get('leave_days')
        if leaveapplication.approval == 'approved':
            leaveobject = Leave(leave_application=leave_application,start=start,end=end,leave_days=leave_days)
            leaveobject.save()
            # update leave assignment days
            leave_assignment = LeaveAssignment.objects.get(id=leaveapplication.leave_assignment_id)
            days_left = leave_assignment.leave_days - leaveobject.leave_days
        
            LeaveAssignment.objects.filter(id=leaveapplication.leave_assignment_id).update(leave_days=days_left)


        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:leave_applications'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Leave Application Decision  successfully Saved.')
        return redirect("hrm:leave_applications")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    def get_initial(self, *args, **kwargs):
        initial = super(ApproveLeaveApplicationView, self).get_initial(**kwargs)
        application_id = self.kwargs['pk']
        leave_application = LeaveApplication.objects.get(id=application_id)
        initial['leave_days'] = leave_application.leave_days_requested
        initial['start'] = leave_application.from_date
        initial['end'] = leave_application.end_date
        
        return initial

    def get_context_data(self, **kwargs):
        context = super(ApproveLeaveApplicationView, self).get_context_data(**kwargs)
        application_id = self.kwargs['pk']
       
        context['leave']= self.get_object()
       
        return context


class ApprovedLeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leave applications.
    """
    #queryset = LeaveApplication.objects.all().order_by('-id')
    serializer_class = ApprovedLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields =['leave_application__leave_assignment__leave_type__leave_name','leave_application__staff__first_name','leave_application__staff__last_name','start','end','leave_days']

    def get_queryset(self):
        """
        This view should return a list of all the approved leave
        for the currently authenticated user.
        """
        user = self.request.user
        queries= Leave.objects.all().order_by('-id')

        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administrative/HR').exists():
            queryset = queries
        else:
            staff = StaffProfile.objects.get(user=user)
            leave_applications = LeaveApplication.filter(staff__in=staff)
            queryset = queries.filter(leave_application__in=leave_applications)

        return queryset

class ApprovedLeavesListView(MenuMixin, LoginRequiredMixin, TemplateView):
    template_name = "approved_leave_applications.html"
    current_menu_item = 'leaves'

# month6 appraisal viewset
class AppraisalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Appraisal model.
    """
    #queryset = LeaveApplication.objects.all().order_by('-id')
    serializer_class = Month6AppraisalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields =['current_job_title','staff__first_name','staff__last_name','supervisor__first_name','supervisor__last_name','implementation_activites','supervisor_comment','staff_comment','deputy_executive_comment','implementation_activites2']

    def get_queryset(self):
        """
        This view should return a list of all the appraisals
        for the currently authenticated staff.
        """
        user = self.request.user
        queries= Month6Appraisal.objects.order_by('-id')

        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administrative/HR').exists():
            queryset = queries
        else:
            staff = StaffProfile.objects.get(user=user)
            queryset = queries.filter(staff__in=staff)

        return queryset

class Month6AppraisalListView(MenuMixin, LoginRequiredMixin, TemplateView):
    template_name = "month6_appraisals.html"
    current_menu_item = 'Appraisals'

# six month appraisal create view 

class CreateMonth6AppraisalView(LoginRequiredMixin, CreateView):
    model = Month6Appraisal
    form_class = Month6AppraisalForm
    template_name = "create_month_six_appraisal.html"

    def dispatch(self, request, *args, **kwargs):

        return super(CreateMonth6AppraisalView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateMonth6AppraisalView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        self.activies = Month6AppraisalActivityFormSet(request.POST, prefix='activities_set')
        self.planned_activities = Month6PlannedAppraisalActivityFormSet(request.POST, prefix='planned_activities_set')
        form = self.get_form()
        formsets_valid = (
                    self.activies.is_valid(),
                    self.planned_activities.is_valid(),
            )
        if form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            print(self.activies.errors)
            print(self.planned_activities.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save appraisal
        appraisal = form.save(commit=False)
        staff = StaffProfile.objects.get(user=self.request.user)
        appraisal.staff = staff
        appraisal.save()
        self.activies.instance = appraisal
        self.activies.save()
        self.planned_activities.instance = appraisal
        self.planned_activities.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'hrm:month6_appraisals'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Staff Six Month Appraisal Submitted successfully.')
        return redirect("hrm:month6_appraisals")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form, dependants=self.activies, alevel=self.planned_activities),

        )
 
    def get_context_data(self, **kwargs):
        context = super(CreateMonth6AppraisalView, self).get_context_data(**kwargs)
        context["form"] = context["form"]
        context["activity_form_set"] = context.get('activies') or Month6AppraisalActivityFormSet(prefix="activities_set")
        context["planned_activities_set"] = context.get('planned_activites') or Month6PlannedAppraisalActivityFormSet(prefix="planned_activities_set")

        return context