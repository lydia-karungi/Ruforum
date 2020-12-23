from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from hrm.models import Department

from .models import (
    Unit, Sourceoffunding, Resultarea, FinancialYear, Workplan,
    Activity, Expectedoutput, Task, Indicator,ActivityOutput,TaskReport,FrameWorkUnit,Framework
    ,FrameworkResult
)

from contacts.models import User


from .forms import (
    UnitForm, SourceoffundingForm, ResultareaForm, FinancialYearForm,
    WorkplanForm, ActivityForm, ExpectedoutputForm, TaskForm,
    IndicatorForm,ActivityOutputForm,TaskReportForm,FrameWorkUnitForm,FrameworkForm,FrameworkResultForm
)

from navutils import MenuMixin
from django.contrib import messages


class UnitsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Unit
    context_object_name = "unit_list"
    template_name = "units.html"
    current_menu_item = 'units'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('unit_name'):
                queryset = queryset.filter(
                    Q(unit_name__icontains=request_post.get('unit_name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(UnitsListView, self).get_context_data(**kwargs)

        #open_units = self.get_queryset().filter(status='open')
        #close_units = self.get_queryset().filter(status='close')
        context["units"] = self.get_queryset().order_by('unit_name')



        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('unit_name', None):
            context["unit_name"] = self.request.POST.getlist('unit_name')

        search = False
        if (
            self.request.POST.get('applicant_name') or self.request.POST.get('status') or
            self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('unit_name'):
            unit_name__icontains = self.request.POST.get('unit_name')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# methoding for creating a unit
class CreateUnitView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "create_unit.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateUnitView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateUnitView, self).get_form_kwargs()
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
        # Save Unit
        unitobject = form.save(commit=False)

        unitobject.created_by = self.request.user

        unitobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_unit")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:unit_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Unit was created successfully.')
        return redirect("pme:unit_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateUnitView, self).get_context_data(**kwargs)
        context["unit_form"] = context["form"]

        return context


#unit details
class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Unit
    context_object_name = "unitrecord"
    template_name = "view_unit.html"

    def get_context_data(self, **kwargs):
        context = super(UnitDetailView, self).get_context_data(**kwargs)
        unitrecord = context["unitrecord"]
        return context


#update unit method
class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "create_unit.html"

    def dispatch(self, request, *args, **kwargs):
        return super(UnitUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UnitUpdateView, self).get_form_kwargs()
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
                'pme:unit_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Unit updated successfully.')
        return redirect("pme:unit_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(UnitUpdateView, self).get_context_data(**kwargs)
        context["unitobj"] = self.object
        context["unitform"] = context["form"]
        return context


#Delete unit
class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = 'view_unit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:unit_list")


class SourceoffundingsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Sourceoffunding
    context_object_name = "sourceoffunding_list"
    template_name = "sourceoffundings.html"
    current_menu_item = 'sourceoffundings'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('sourceoffunding_name'):
                queryset = queryset.filter(
                    Q(fund_name__icontains=request_post.get('sourceoffunding_name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SourceoffundingsListView, self).get_context_data(**kwargs)
        context["sourceoffundings"] = self.get_queryset().order_by('fund_name')

        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


#create new development partner
class CreateSourceoffundingView(LoginRequiredMixin, CreateView):
    model = Sourceoffunding
    form_class = SourceoffundingForm
    template_name = "create_sourceoffunding.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateSourceoffundingView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateSourceoffundingView, self).get_form_kwargs()
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
        # Save Sourceoffunding
        sourceoffundingobject = form.save(commit=False)

        sourceoffundingobject.created_by = self.request.user

        sourceoffundingobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_sourceoffunding")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:sourceoffunding_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Source of funding was created successfully.')
        return redirect("pme:sourceoffunding_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateSourceoffundingView, self).get_context_data(**kwargs)
        context["sourceoffunding_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class SourceoffundingDetailView(LoginRequiredMixin, DetailView):
    model = Sourceoffunding
    context_object_name = "sourceoffundingrecord"
    template_name = "view_sourceoffunding.html"

    def get_context_data(self, **kwargs):
        context = super(SourceoffundingDetailView, self).get_context_data(**kwargs)
        sourceoffundingrecord = context["sourceoffundingrecord"]
        return context


#update source of funding
class SourceoffundingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sourceoffunding
    form_class = SourceoffundingForm
    template_name = "create_sourceoffunding.html"

    def dispatch(self, request, *args, **kwargs):
        return super(SourceoffundingUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SourceoffundingUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Sourceoffunding
        sourceoffundingobject = form.save(commit=False)
        sourceoffundingobject.save()
        #sourceoffundingobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:sourceoffunding_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Source of funding updated successfully.')
        return redirect("pme:sourceoffunding_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(SourceoffundingUpdateView, self).get_context_data(**kwargs)
        context["sourceoffundingobj"] = self.object
        context["sourceoffundingform"] = context["form"]
        return context


#Delete development partner
class SourceoffundingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sourceoffunding
    template_name = 'view_sourceoffunding.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:sourceoffunding_list")


class ResultareasListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Resultarea
    context_object_name = "resultarea_list"
    template_name = "resultareas.html"
    current_menu_item = 'resultareas'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('resultarea_name'):
                queryset = queryset.filter(
                    Q(result_area__icontains=request_post.get('resultarea_name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ResultareasListView, self).get_context_data(**kwargs)
        context["resultareas"] = self.get_queryset().order_by('result_area')



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


#class CreateResultareaView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateResultareaView(LoginRequiredMixin, CreateView):
    model = Resultarea
    form_class = ResultareaForm
    template_name = "create_resultarea.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateResultareaView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateResultareaView, self).get_form_kwargs()
        #kwargs.update({"resultarea": True})
        #kwargs.update({"request_user": self.request.user})
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
        # Save Resultarea
        resultareaobject = form.save(commit=False)

        resultareaobject.created_by = self.request.user

        resultareaobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_resultarea")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:resultarea_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Result Area was created successfully.')
        return redirect("pme:resultarea_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateResultareaView, self).get_context_data(**kwargs)
        context["resultarea_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class ResultareaDetailView(LoginRequiredMixin, DetailView):
    model = Resultarea
    context_object_name = "resultarearecord"
    template_name = "view_resultarea.html"

    def get_context_data(self, **kwargs):
        context = super(ResultareaDetailView, self).get_context_data(**kwargs)
        resultarearecord = context["resultarearecord"]
        return context


#SalesAccessRequiredMixin,
class ResultareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Resultarea
    form_class = ResultareaForm
    template_name = "create_resultarea.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ResultareaUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ResultareaUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Resultarea
        resultareaobject = form.save(commit=False)
        resultareaobject.save()
        #resultareaobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:resultarea_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Result Area was updated successfully.')
        return redirect("pme:resultarea_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ResultareaUpdateView, self).get_context_data(**kwargs)
        context["resultareaobj"] = self.object
        context["resultareaform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class ResultareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Resultarea
    template_name = 'view_resultarea.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:resultarea_list")


class FinancialYearsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = FinancialYear
    context_object_name = "financialyear_list"
    template_name = "financialyears.html"
    current_menu_item = 'financialyears'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('start_date'):
                queryset = queryset.filter(
                    start_date__icontains=request_post.get('start_date'))
            if request_post.get('end_date'):
                queryset = queryset.filter(
                    end_date__icontains=request_post.get('end_date'))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(FinancialYearsListView, self).get_context_data(**kwargs)

        context["financialyears"] = self.get_queryset().order_by('-start_date')



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


#class CreateFinancialYearView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateFinancialYearView(LoginRequiredMixin, CreateView):
    model = FinancialYear
    form_class = FinancialYearForm
    template_name = "create_financialyear.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateFinancialYearView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFinancialYearView, self).get_form_kwargs()
        #kwargs.update({"financialyear": True})
        #kwargs.update({"request_user": self.request.user})
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
        # Save FinancialYear
        financialyearobject = form.save(commit=False)

        financialyearobject.created_by = self.request.user

        financialyearobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_financialyear")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:financialyear_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Financial year was created successfully.')
        return redirect("pme:financialyear_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFinancialYearView, self).get_context_data(**kwargs)
        context["financialyear_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class FinancialYearDetailView(LoginRequiredMixin, DetailView):
    model = FinancialYear
    context_object_name = "financialyearrecord"
    template_name = "view_financialyear.html"

    def get_context_data(self, **kwargs):
        context = super(FinancialYearDetailView, self).get_context_data(**kwargs)
        financialyearrecord = context["financialyearrecord"]
        return context


#SalesAccessRequiredMixin,
class FinancialYearUpdateView(LoginRequiredMixin, UpdateView):
    model = FinancialYear
    form_class = FinancialYearForm
    template_name = "create_financialyear.html"

    def dispatch(self, request, *args, **kwargs):
        return super(FinancialYearUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FinancialYearUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save FinancialYear
        financialyearobject = form.save(commit=False)
        financialyearobject.save()
        #financialyearobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:financialyear_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Financial year was updated successfully.')
        return redirect("pme:financialyear_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FinancialYearUpdateView, self).get_context_data(**kwargs)
        context["financialyearobj"] = self.object
        context["financialyearform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class FinancialYearDeleteView(LoginRequiredMixin, DeleteView):
    model = FinancialYear
    template_name = 'view_financialyear.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:financialyear_list")


class WorkplansListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Workplan
    context_object_name = "workplan_list"
    template_name = "workplans.html"
    current_menu_item = 'workplans'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('workplan_name'):
                queryset = queryset.filter(
                    workplan_name__icontains=request_post.get('workplan_name'))
          
            if request_post.get('financialyear'):
                queryset = queryset.filter(
                    Q(financial_year=request_post.get('financialyear')))
            if request_post.get('department'):
                queryset = queryset.filter(
                    Q(department=request_post.get('department')))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(WorkplansListView, self).get_context_data(**kwargs)
        context["workplans"] = self.get_queryset().order_by('-financial_year__start_date')
        context["per_page"] = self.request.POST.get('per_page')
        context['financial_years'] = FinancialYear.objects.all()
        context['departments']= Department.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


#class CreateWorkplanView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateWorkplanView(LoginRequiredMixin, CreateView):
    model = Workplan
    form_class = WorkplanForm
    template_name = "create_workplan.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateWorkplanView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateWorkplanView, self).get_form_kwargs()
        #kwargs.update({"workplan": True})
        #kwargs.update({"request_user": self.request.user})
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
        # Save Workplan
        workplanobject = form.save(commit=False)

        workplanobject.created_by = self.request.user

        workplanobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_workplan")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:workplan_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Work Plan was created successfully.')
        return redirect("pme:workplan_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateWorkplanView, self).get_context_data(**kwargs)
        context["workplan_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class WorkplanDetailView(LoginRequiredMixin, DetailView):
    model = Workplan
    context_object_name = "workplanrecord"
    template_name = "view_workplan.html"

    def get_context_data(self, **kwargs):
        context = super(WorkplanDetailView, self).get_context_data(**kwargs)
        workplanrecord = context["workplanrecord"]
        return context


#SalesAccessRequiredMixin,
class WorkplanUpdateView(LoginRequiredMixin, UpdateView):
    model = Workplan
    form_class = WorkplanForm
    template_name = "create_workplan.html"

    def dispatch(self, request, *args, **kwargs):
        return super(WorkplanUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(WorkplanUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Workplan
        workplanobject = form.save(commit=False)
        workplanobject.save()
        #workplanobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:workplan_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Work Plan  updated successfully.')
        return redirect("pme:workplan_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(WorkplanUpdateView, self).get_context_data(**kwargs)
        context["workplanobj"] = self.object
        context["workplan_form"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class WorkplanDeleteView(LoginRequiredMixin, DeleteView):
    model = Workplan
    template_name = 'view_workplan.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:workplan_list")


class ActivitysListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Activity
    context_object_name = "activity_list"
    template_name = "activities.html"
    current_menu_item = 'activitys'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('activity_name'):
                queryset = queryset.filter(
                    Q(activity_name__icontains=request_post.get('activity_name')))

            if request_post.get('workplan'):
                queryset=queryset.filter(
                    Q(workplan=request_post.get('workplan'))
                )
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ActivitysListView, self).get_context_data(**kwargs)

        #open_activitys = self.get_queryset().filter(status='open')
        #close_activitys = self.get_queryset().filter(status='close')
        context["activities"] = self.get_queryset().order_by('activity_name')



        context["per_page"] = self.request.POST.get('per_page')
        #tag_ids = list(set(Activity.objects.values_list('tags', flat=True)))
        #context["tags"] = Tags.objects.filter(id__in=tag_ids)
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
        context['workplans'] = Workplan.objects.all()
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


#class CreateActivityView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateActivityView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "create_activity.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateActivityView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateActivityView, self).get_form_kwargs()
        #kwargs.update({"activity": True})
        #kwargs.update({"request_user": self.request.user})
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
        # Save Activity
        activityobject = form.save(commit=False)

        activityobject.created_by = self.request.user

        activityobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_activity")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:activity_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Activity  was created successfully.')
        return redirect("pme:activity_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateActivityView, self).get_context_data(**kwargs)
        context["activity_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    context_object_name = "activityrecord"
    template_name = "view_activity.html"

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        activityrecord = context["activityrecord"]
        return context


#SalesAccessRequiredMixin,
class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "create_activity.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ActivityUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ActivityUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Activity
        activityobject = form.save(commit=False)
        activityobject.save()
        #activityobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:activity_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Activity  updated successfully.')
        return redirect("pme:activity_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ActivityUpdateView, self).get_context_data(**kwargs)
        context["activityobj"] = self.object
        context["activityform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'view_activity.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:activity_list")


class ExpectedoutputsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Expectedoutput
    context_object_name = "output_list"
    template_name = "outputs.html"
    current_menu_item = 'outputs'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('activity'):
                queryset = queryset.filter(
                    Q(activity=request_post.get('activity')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ExpectedoutputsListView, self).get_context_data(**kwargs)

        context["outputs"] = self.get_queryset().order_by('output')

        context["per_page"] = self.request.POST.get('per_page')
        context["activities"] = Activity.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


#Expected output from activities
class CreateExpectedoutputView(LoginRequiredMixin, CreateView):
    model = Expectedoutput
    form_class = ExpectedoutputForm
    template_name = "create_output.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateExpectedoutputView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateExpectedoutputView, self).get_form_kwargs()
        #kwargs.update({"output": True})
        #kwargs.update({"request_user": self.request.user})
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
        # Save Expectedoutput
        outputobject = form.save(commit=False)

        outputobject.created_by = self.request.user

        outputobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_output")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:output_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Expected output was created successfully.')
        return redirect("pme:output_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateExpectedoutputView, self).get_context_data(**kwargs)
        context["output_form"] = context["form"]

        return context


#details of expected outcome
class ExpectedoutputDetailView(LoginRequiredMixin, DetailView):
    model = Expectedoutput
    context_object_name = "outputrecord"
    template_name = "view_output.html"

    def get_context_data(self, **kwargs):
        context = super(ExpectedoutputDetailView, self).get_context_data(**kwargs)
        outputrecord = context["outputrecord"]
        return context


#SalesAccessRequiredMixin,
class ExpectedoutputUpdateView(LoginRequiredMixin, UpdateView):
    model = Expectedoutput
    form_class = ExpectedoutputForm
    template_name = "create_output.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ExpectedoutputUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ExpectedoutputUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Expectedoutput
        outputobject = form.save(commit=False)
        outputobject.save()
        #outputobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:output_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Expected output updated successfully.')
        return redirect("pme:output_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ExpectedoutputUpdateView, self).get_context_data(**kwargs)
        context["outputobj"] = self.object
        context["outputform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class ExpectedoutputDeleteView(LoginRequiredMixin, DeleteView):
    model = Expectedoutput
    template_name = 'view_output.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:output_list")



class TasksListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks.html"
    current_menu_item = 'tasks'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('task_name'):
                queryset = queryset.filter(
                    Q(task_name__icontains=request_post.get('task_name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TasksListView, self).get_context_data(**kwargs)

        #open_tasks = self.get_queryset().filter(status='open')
        #close_tasks = self.get_queryset().filter(status='close')
        context["tasks"] = self.get_queryset().order_by('task_name')
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


#class CreateTaskView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "create_task.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateTaskView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateTaskView, self).get_form_kwargs()
        #kwargs.update({"task": True})
        #kwargs.update({"request_user": self.request.user})
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
        # Save Task
        taskobject = form.save(commit=False)

        taskobject.created_by = self.request.user

        taskobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_task")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:task_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Task was created successfully.')
        return redirect("pme:task_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateTaskView, self).get_context_data(**kwargs)
        context["task_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "taskrecord"
    template_name = "view_task.html"

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        taskrecord = context["taskrecord"]
        return context


#SalesAccessRequiredMixin,
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "create_task.html"

    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Task
        taskobject = form.save(commit=False)
        taskobject.save()
        #taskobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:task_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Task  updated successfully.')
        return redirect("pme:task_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)
        context["taskobj"] = self.object
        context["taskform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'view_task.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:task_list")


class IndicatorsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Indicator
    context_object_name = "indicator_list"
    template_name = "indicators.html"
    current_menu_item = 'indicators'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('activity'):
                queryset = queryset.filter(
                    Q(activity=request_post.get('activity')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndicatorsListView, self).get_context_data(**kwargs)
        context["activities"] = Activity.objects.all()
        context["indicators"] = self.get_queryset().order_by('indicator')
        context["per_page"] = self.request.POST.get('per_page')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


#class CreateIndicatorView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateIndicatorView(LoginRequiredMixin, CreateView):
    model = Indicator
    form_class = IndicatorForm
    template_name = "create_indicator.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateIndicatorView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateIndicatorView, self).get_form_kwargs()
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
        # Save Indicator
        indicatorobject = form.save(commit=False)

        indicatorobject.created_by = self.request.user

        indicatorobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_indicator")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:indicator_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Indicator was created successfully.')
        return redirect("pme:indicator_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateIndicatorView, self).get_context_data(**kwargs)
        context["indicator_form"] = context["form"]

        return context


#SalesAccessRequiredMixin,
class IndicatorDetailView(LoginRequiredMixin, DetailView):
    model = Indicator
    context_object_name = "indicatorrecord"
    template_name = "view_indicator.html"

    def get_context_data(self, **kwargs):
        context = super(IndicatorDetailView, self).get_context_data(**kwargs)
        indicatorrecord = context["indicatorrecord"]
        return context


#SalesAccessRequiredMixin,
class IndicatorUpdateView(LoginRequiredMixin, UpdateView):
    model = Indicator
    form_class = IndicatorForm
    template_name = "create_indicator.html"

    def dispatch(self, request, *args, **kwargs):
        return super(IndicatorUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(IndicatorUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Indicator
        indicatorobject = form.save(commit=False)
        indicatorobject.save()
        #indicatorobject.tags.clear()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:indicator_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Indicator updated successfully.')
        return redirect("pme:indicator_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(IndicatorUpdateView, self).get_context_data(**kwargs)
        context["indicatorobj"] = self.object
        context["indicatorform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class IndicatorDeleteView(LoginRequiredMixin, DeleteView):
    model = Indicator
    template_name = 'view_indicator.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:indicator_list")

#List view for activity outcome
class ActivityOutputListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = ActivityOutput
    context_object_name = "actvitityoutput_list"
    template_name = "activityoutput.html"
    current_menu_item = 'outputs'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('activity'):
                queryset = queryset.filter(
                    Q(activity=request_post.get('activity')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ActivityOutputListView, self).get_context_data(**kwargs)
        context["outputs"] = self.get_queryset().order_by('output')

        context["per_page"] = self.request.POST.get('per_page')

        context["activities"] = Activity.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# create activity outcome
class CreateActivityoutputView(LoginRequiredMixin, CreateView):
    model = ActivityOutput
    form_class = ActivityOutputForm
    template_name = "create_activityoutput.html"

    def dispatch(self, request, *args, **kwargs):

        return super(CreateActivityoutputView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateActivityoutputView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        # redirect user to the form again in case its invalid
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # save the activity out put
        outputobject = form.save(commit=False)

        outputobject.created_by = self.request.user

        outputobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:new_activityoutput")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:activity_output_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Activity output was created successfully.')
        return redirect("pme:activity_output_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateActivityoutputView, self).get_context_data(**kwargs)
        context["output_form"] = context["form"]

        return context


#edit activity output
class ActivityoutputUpdateView(LoginRequiredMixin, UpdateView):
    model = ActivityOutput
    form_class = ActivityOutputForm
    template_name = "create_activityoutput.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ActivityoutputUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ActivityoutputUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Expectedoutput
        outputobject = form.save(commit=False)
        outputobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:activity_output_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Activity output updated successfully.')
        return redirect("pme:activity_output_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ActivityoutputUpdateView, self).get_context_data(**kwargs)
        context["outputobj"] = self.object
        context["outputform"] = context["form"]
        return context


#SalesAccessRequiredMixin,
class ActivityoutputDeleteView(LoginRequiredMixin, DeleteView):
    model = ActivityOutput
    template_name = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:activity_output_list")


# create task report
class CreateTaskReportView(LoginRequiredMixin, CreateView):
    model = TaskReport
    form_class = TaskReportForm
    template_name = "create_report.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateTaskReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateTaskReportView, self).get_form_kwargs()
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
        #
        reportobject = form.save(commit=False)

        reportobject.created_by = self.request.user

        reportobject.save()
        messages.add_message(self.request, messages.SUCCESS, 'Task Report created successfully.')
        return redirect("pme:task_list")

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateTaskReportView, self).get_context_data(**kwargs)
        context["form"] = context["form"]
        context["task"]= Task.objects.get(pk=self.kwargs['task_pk'])


        return context


#task report list
class TaskReportListView(LoginRequiredMixin, TemplateView):
    model = TaskReport
    context_object_name = "report_obj_list"
    template_name = "report_list.html"

    def get_queryset(self):
        queryset = self.model.objects.order_by('status')
        request_post = self.request.POST
        if request_post:
            if request_post.get('status'):
                queryset = queryset.filter(
                   status__icontains=request_post.get('status'))
            if request_post.get('has_file'):
                queryset = queryset.filter(
                    has_file__icontains=request_post.get('has_file'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(TaskReportListView, self).get_context_data(**kwargs)
        context["report_obj_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        search = False
        if (
            self.request.POST.get('status') or
            self.request.POST.get('has_file')
        ):
            search = True
        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

# edit task report
class TaskReportUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskReport
    form_class = TaskReportForm
    template_name = "edit_report.html"

    def dispatch(self, request, *args, **kwargs):
        return super(TaskReportUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskReportUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Task report
        taskreportobject = form.save(commit=False)
        taskreportobject.created_by = self.request.user
        taskreportobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:task_reports'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Task Report updated successfully.')
        return redirect("pme:task_reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(TaskReportUpdateView, self).get_context_data(**kwargs)
        context["taskreportobj"] = self.object
        context["form"] = context["form"]
        return context

#Delete task report
class TaskReportDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskReport
    template_name = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("pme:task_reports")

#framework unit list
class FrameworkUnitsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = FrameWorkUnit
    context_object_name = "unit_list"
    template_name = "framework_units.html"
    current_menu_item = 'units'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('unit_name'):
                queryset = queryset.filter(
                    Q(unit__icontains=request_post.get('unit_name')))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(FrameworkUnitsListView, self).get_context_data(**kwargs)

        #open_units = self.get_queryset().filter(status='open')
        #close_units = self.get_queryset().filter(status='close')
        context["units"] = self.get_queryset().order_by('unit')



        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('unit', None):
            context["unit"] = self.request.POST.getlist('unit')

        search = False
        if (
            self.request.POST.get('applicant_name') or self.request.POST.get('status') or
            self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('unit_name'):
            unit__icontains = self.request.POST.get('unit_name')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
# create framework unit
class CreateFrameworkUnitView(LoginRequiredMixin, CreateView):
    model = FrameWorkUnit
    form_class = FrameWorkUnitForm
    template_name = "create_framework_unit.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateFrameworkUnitView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFrameworkUnitView, self).get_form_kwargs()
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
        # Save Unit
        unitobject = form.save(commit=False)

        #unitobject.created_by = self.request.user

        unitobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:framework_unit_list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:framework_unit_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Framework unit created successfully.')
        return redirect("pme:framework_unit_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFrameworkUnitView, self).get_context_data(**kwargs)
        context["unit_form"] = context["form"]

        return context
#update unit method
class FrameworkUnitUpdateView(LoginRequiredMixin, UpdateView):
    model = FrameWorkUnit
    form_class = FrameWorkUnitForm
    template_name = "create_framework_unit.html"

    def dispatch(self, request, *args, **kwargs):
        return super(FrameworkUnitUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FrameworkUnitUpdateView, self).get_form_kwargs()
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
                'pme:framework_unit_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Framework unit updated successfully.')
        return redirect("pme:framework_unit_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FrameworkUnitUpdateView, self).get_context_data(**kwargs)
        context["unitobj"] = self.object
        context["unitform"] = context["form"]
        return context


#Delete unit
class FrameworkUnitDeleteView(LoginRequiredMixin, DeleteView):
    model = FrameWorkUnit
    template_name = 'view_unit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("pme:framework_unit_list")


# Framework
class FrameworkListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Framework
    context_object_name = "framework_list"
    template_name = "frameworks.html"
    current_menu_item = 'framework'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('framework_name'):
                queryset = queryset.filter(
                    particular__icontains=request_post.get('framework_name'))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(FrameworkListView, self).get_context_data(**kwargs)
        context["framework"] = self.get_queryset().order_by('particular')



        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('framework', None):
            context["framework"] = self.request.POST.getlist('framework')

        tab_status = 'Open'
        if self.request.POST.get('unit_name'):
            particular__icontains = self.request.POST.get('unit_name')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
# create framework unit
class CreateFrameworkView(LoginRequiredMixin, CreateView):
    model = Framework
    form_class = FrameworkForm
    template_name = "create_framework.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateFrameworkView, self).dispatch(request, *args, **kwargs)

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
        # Save Unit
        unitobject = form.save(commit=False)

        #unitobject.created_by = self.request.user

        unitobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:framework_list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:framework_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Framework created successfully.')
        return redirect("pme:framework_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFrameworkView, self).get_context_data(**kwargs)
        context["unit_form"] = context["form"]

        return context
#update unit method
class FrameworkUpdateView(LoginRequiredMixin, UpdateView):
    model = Framework
    form_class = FrameworkForm
    template_name = "create_framework.html"

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
                'pme:framework_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Framework  updated successfully.')
        return redirect("pme:framework_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FrameworkUpdateView, self).get_context_data(**kwargs)
        context["unitobj"] = self.object
        context["unitform"] = context["form"]
        return context


#Delete unit
class FrameworkDeleteView(LoginRequiredMixin, DeleteView):
    model = Framework
    template_name = 'view_unit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("pme:framework_list")


# Framwork results

class FrameworkResultListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = FrameworkResult
    context_object_name = "framework_result_list"
    template_name = "framework_results.html"
    current_menu_item = 'framework_results'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('framework_name'):
                queryset = queryset.filter(
                    key_performance_indicator__icontains=request_post.get('framework_name'))
            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(FrameworkResultListView, self).get_context_data(**kwargs)
        context["framework_result_list"] = self.get_queryset().order_by('framework')



        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('framework', None):
            context["framework"] = self.request.POST.getlist('framework')

        tab_status = 'Open'
        if self.request.POST.get('unit_name'):
            key_performance_indicator__icontains = self.request.POST.get('unit_name')
        context['tab_status'] = tab_status
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
# create framework unit
class CreateFrameworkResultView(LoginRequiredMixin, CreateView):
    model = FrameworkResult
    form_class = FrameworkResultForm
    template_name = "create_framework_result.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateFrameworkResultView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFrameworkResultView, self).get_form_kwargs()
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
        # Save Unit
        unitobject = form.save(commit=False)

        unitobject.save()


        if self.request.POST.get("savenewform"):
            return redirect("pme:framework_result_list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'pme:framework_result_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Framework Result created successfully.')
        return redirect("pme:framework_result_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFrameworkResultView, self).get_context_data(**kwargs)
        context["form"] = context["form"]

        return context
#update framework result method
class FrameworkResultUpdateView(LoginRequiredMixin, UpdateView):
    model = FrameworkResult
    form_class = FrameworkResultForm
    template_name = "create_framework_result.html"

    def dispatch(self, request, *args, **kwargs):
        return super(FrameworkResultUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FrameworkResultUpdateView, self).get_form_kwargs()
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
                'pme:framework_result_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Framework Result updated successfully.')
        return redirect("pme:framework_result_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FrameworkResultUpdateView, self).get_context_data(**kwargs)
        context["unitobj"] = self.object
        context["unitform"] = context["form"]
        return context


#Delete unit
class FrameworkResultDeleteView(LoginRequiredMixin, DeleteView):
    model = FrameworkResult
    template_name = 'view_framework_result.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("pme:framework_result_list")
    
class FrameworkResultDetailView(LoginRequiredMixin, DetailView):
    model = FrameworkResult
    context_object_name = "resultrecord"
    template_name = "view_framework_result.html"

    def get_context_data(self, **kwargs):
        context = super(FrameworkResultDetailView, self).get_context_data(**kwargs)
        resultrecord = context["resultrecord"]
        return context