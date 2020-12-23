from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)
from common.utils import has_group
from grants.models import Grant, GrantComment#, Tags, Email
from grants_applications.models import Grantapplication
from grants_reports.models import (FirstReport, FirstStudentReport, Month12Report, Studentmonth12Report
, Studentmonth18Report, Studentmonth24Report, LastStudentReport, LastReport, Month24Report, Month18Report,
                                   RelevantPictures12, Month30Report, Studentmonth30Report, Month36Report,
                                   Studentmonth36Report, Month42Report, Studentmonth42Report, RelevantPictures18,
                                   RelevantPictures24, RelevantPictures30, RelevantPictures36, RelevantPictures42,
                                   Month48Report, Studentmonth48Report, RelevantPictures48, Month54Report,
                                   RelevantPictures54, Studentmonth54Report, Month60Report, Studentmonth60Report,
                                   RelevantPictures60, RelevantPictures66, Studentmonth66Report, Month66Report,
                                   Month72Report, RelevantPictures72, Studentmonth72Report, Month78Report,
                                   RelevantPictures78, Studentmonth78Report, Month84Report, Studentmonth84Report,
                                   RelevantPictures84, RelevantPictures90, Studentmonth90Report, Month90Report,
                                   Month96Report, RelevantPictures96, Studentmonth96Report, Month102Report,
                                   RelevantPictures102, Studentmonth102Report, Month108Report, RelevantPictures108,
                                   Studentmonth108Report, PIPublications, StudentPublication, Technology, TempReport)
from contacts.models import User
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil import relativedelta
from django.contrib.sites.shortcuts import get_current_site

from .forms import GrantForm, GrantCommentForm,GrantApprovalForm
from grants_reports.forms import (Studentmonth6ReportFormSet, Month6ReportForm, Month12ReportForm
, Studentmonth12ReportFormSet, Studentmonth18ReportFormSet, Month18ReportForm, Studentmonth24ReportFormSet,
                                  Month24ReportForm
, Studentmonth30ReportFormSet, Month30ReportForm, Month36ReportForm, Studentmonth36ReportFormSet, Month42ReportForm,
                                  Studentmonth42ReportFormSet, Month48ReportForm, Studentmonth48ReportFormSet,
                                  Studentmonth54ReportFormSet, Month54ReportForm, Studentmonth60ReportFormSet,
                                  Month60ReportForm, Studentmonth66ReportFormSet, Month66ReportForm,
                                  Studentmonth72ReportFormSet, Month72ReportForm, Studentmonth78ReportFormSet,
                                  Month78ReportForm, Month84ReportForm, Studentmonth84ReportFormSet,
                                  Studentmonth90ReportFormSet, Month90ReportForm, Studentmonth96ReportFormSet,
                                  Month96ReportForm, Studentmonth102ReportFormSet, Month102ReportForm,
                                  Month108ReportForm, Studentmonth108ReportFormSet, LastStudentReportFormSet)
import datetime
from django.contrib import messages
from datetime import date
import logging
log = logging.getLogger('RIMS')


class GrantsListView(LoginRequiredMixin, TemplateView):
    model = Grant
    context_object_name = "grants_list"
    template_name = "grants.html"

    def get_queryset(self):
        queryset = self.model.objects.order_by('-pk')
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('hide_expired'):
                today = datetime.date.today()
                queryset = queryset.filter(Q(end_date__gte=today, new_end_date__isnull=True) | Q(new_end_date__gte=today, new_end_date__isnull=False))

            if request_post.get('date_range_start'):
                queryset = queryset.filter(
                    start_date__gte=request_post.get('date_range_start'))
            if request_post.get('date_range_end'):
                queryset = queryset.filter(
                    Q(end_date__lte=request_post.get('date_range_end')) | Q(new_end_date__lte=request_post.get('date_range_end')))

            if request_post.get('grant_id'):
                queryset = queryset.filter(
                    grant_id__icontains=request_post.get('grant_id'))
            if request_post.get('call'):
                queryset = queryset.filter(
                    grant_application__call__call_id__icontains=request_post.get('call'))
            if request_post.get('title'):
                queryset = queryset.filter(
                    title__contains=request_post.get('title'))
            if request_post.get('grant_application'):
                queryset = queryset.filter(
                    grant_application__icontains=request_post.get('grant_application'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))
            if request_post.get('pi'):
                queryset = queryset.filter(
                    Q(pi__first_name__icontains=request_post.get('pi')) | Q(pi__last_name__icontains=request_post.get('pi')))

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GrantsListView, self).get_context_data(**kwargs)
        grant_applications = Grantapplication.objects.all()
        application_approvals = Grantapplication.objects.all().order_by('-pk')
        pi_application_approvals=Grantapplication.objects.filter(user=self.request.user)
        context["grants_list"] = self.get_queryset()
        context["grant_applications"] = grant_applications
        pi_applications = Grantapplication.objects.filter(user=self.request.user)
        context["pi_applications"] = grant_applications
        context["application_approvals"] = application_approvals
        context['pi_application_approvals']=pi_application_approvals
        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
            self.request.POST.get('name') or self.request.POST.get('city') or
            self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('tab_status'):
            tab_status = self.request.POST.get('tab_status')
        context['tab_status'] = tab_status

        # other things we'll need in the templates...
        context['metrics'] = {
                'active_grants': Grant.count_all_active()
                }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateGrantView(LoginRequiredMixin, CreateView):
    model = Grant
    form_class = GrantForm
    template_name = "create_grant.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateGrantView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateGrantView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            log.error(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Grant
        grantobject = form.save(commit=False)

        grantobject.created_by = self.request.user

        grantobject.save()
        form.save_m2m()
        if self.request.POST.get("savenewform"):
            return redirect("grants:new_account")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grants:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant was created successfully.')
        return redirect("grants:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateGrantView, self).get_context_data(**kwargs)
        context["grant_form"] = context["form"]
        return context


class GrantCommentsView(FormView):
    form_class = GrantCommentForm

    def post(self, request, *args, **kwargs):
        gc_form = GrantCommentForm(request.POST)
        try:
            gc_form.is_valid()
        except:
            pass
        gc = GrantComment(comment=gc_form.cleaned_data['comment'])
        gc.grant = Grant.objects.get(id=gc_form.cleaned_data.get('grant'))
        gc.created_by = User.objects.get(id=gc_form.cleaned_data.get('created_by'))
        gc.save()
        return HttpResponseRedirect(reverse("grants:review_grant",kwargs={"pk": gc.grant.id}))

    def get_success_url(self):
        return reverse("grant:review_grant",kwargs={"pk": self.grant_id})


class GrantReviewView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "review_grant.html"

    def get_context_data(self, **kwargs):
        context = super(GrantReviewView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        context["comments_form"] = GrantCommentForm
        grantrecord = context["grant"]
        comment_permission = True if (
            self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False
        context['comment_permission'] = comment_permission,
        return context


class GrantUpdateView(LoginRequiredMixin, UpdateView):
    model = Grant
    form_class = GrantForm
    template_name = "create_grant.html"

    def get_form_kwargs(self):
        kwargs = super(GrantUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Grant
        grantobject = form.save(commit=False)
        grantobject.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grants:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant was updated successfully.')
        return redirect("grants:list")

    def form_invalid(self, form):
        print(form.errors)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(GrantUpdateView, self).get_context_data(**kwargs)
        context["grantobj"] = self.object
        '''
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != context['grantobj'].created_by:
                raise PermissionDenied
        '''
        context["grant_form"] = context["form"]
        return context

# delete grant 
class GrantDeleteView(LoginRequiredMixin, DeleteView):
    model = Grant
    template_name = 'grants.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("grants:list")


class Month6View(LoginRequiredMixin, DetailView):
    model = FirstReport
    context_object_name = "report"
    template_name = "month6.html"

    def get_context_data(self, **kwargs):
        context = super(Month6View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month6ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth6ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports":FirstStudentReport.objects.filter(month_6_report=report),
            "user": self.request.user
        })
        print(context)

        return context


class Month12View(LoginRequiredMixin, DetailView):
    model = Month12Report
    context_object_name = "report"
    template_name = "month12.html"

    def get_context_data(self, **kwargs):
        context = super(Month12View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month6ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth12ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth12Report.objects.filter(month_12_report=report),
            'project_images': RelevantPictures12.objects.filter(grant_report=report)
        })
        print(context)

        return context


class Month18View(LoginRequiredMixin, DetailView):
    model = Month18Report
    context_object_name = "report"
    template_name = "month18.html"

    def get_context_data(self, **kwargs):
        context = super(Month18View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month18ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth18ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports":Studentmonth18Report.objects.filter(month_18_report=report),
            'project_images': RelevantPictures18.objects.filter(grant_report=report)
        })
        print(context)

        return context


class Month24View(LoginRequiredMixin, DetailView):
    model = Month24Report
    context_object_name = "report"
    template_name = "month24.html"

    def get_context_data(self, **kwargs):
        context = super(Month24View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month24ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth24ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth24Report.objects.filter(month_24_report=report),
            'project_images': RelevantPictures24.objects.filter(grant_report=report)
        })
        print(context)

        return context


class Month30View(LoginRequiredMixin, DetailView):
    model = Month30Report
    context_object_name = "report"
    template_name = "month30.html"

    def get_context_data(self, **kwargs):
        context = super(Month30View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month30ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth30ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth30Report.objects.filter(month_30_report=report),
            'project_images': RelevantPictures30.objects.filter(grant_report=report),
            'month':'month30',
            'accept_url':'accept_fifth_report'
        })
        print(context)

        return context


class Month36View(LoginRequiredMixin, DetailView):
    model = Month36Report
    context_object_name = "report"
    template_name = "month36.html"

    def get_context_data(self, **kwargs):
        context = super(Month36View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month36ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth36ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth36Report.objects.filter(month_36_report=report),
            'project_images': RelevantPictures36.objects.filter(grant_report=report),
            'month':'month36',
            'accept_url':'accept_sixth_report'
        })
        print(context)

        return context


class Month42View(LoginRequiredMixin, DetailView):
    model = Month42Report
    context_object_name = "report"
    template_name = "month42.html"

    def get_context_data(self, **kwargs):
        context = super(Month42View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month42ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth42ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth42Report.objects.filter(month_42_report=report),
            'project_images': RelevantPictures42.objects.filter(grant_report=report),
            'month':'month42',
            'accept_url':'accept_seventh_report'
        })
        print(context)

        return context


class Month48View(LoginRequiredMixin, DetailView):
    model = Month48Report
    context_object_name = "report"
    template_name = "month48.html"

    def get_context_data(self, **kwargs):
        context = super(Month48View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month48ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth48ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth48Report.objects.filter(month_48_report=report),
            'project_images': RelevantPictures48.objects.filter(grant_report=report),
            'month':'month48',
            'accept_url':'accept_eighth_report'
        })
        print(context)

        return context


class Month54View(LoginRequiredMixin, DetailView):
    model = Month54Report
    context_object_name = "report"
    template_name = "month54.html"

    def get_context_data(self, **kwargs):
        context = super(Month54View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month54ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth54ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth54Report.objects.filter(month_54_report=report),
            'project_images': RelevantPictures54.objects.filter(grant_report=report),
            'month':'month54',
            'accept_url':'accept_nineth_report'
        })
        print(context)

        return context


class Month60View(LoginRequiredMixin, DetailView):
    model = Month60Report
    context_object_name = "report"
    template_name = "month60.html"

    def get_context_data(self, **kwargs):
        context = super(Month60View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month60ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth60ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth60Report.objects.filter(month_60_report=report),
            'project_images': RelevantPictures60.objects.filter(grant_report=report),
            'month':'month60',
            'accept_url':'accept_tenth_report'
        })
        print(context)

        return context


class Month66View(LoginRequiredMixin, DetailView):
    model = Month66Report
    context_object_name = "report"
    template_name = "month66.html"

    def get_context_data(self, **kwargs):
        context = super(Month66View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month66ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth66ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth66Report.objects.filter(month_66_report=report),
            'project_images': RelevantPictures66.objects.filter(grant_report=report),
            'month':'month66',
            'accept_url':'accept_eleventh_report'
        })
        print(context)

        return context


class Month72View(LoginRequiredMixin, DetailView):
    model = Month72Report
    context_object_name = "report"
    template_name = "month72.html"

    def get_context_data(self, **kwargs):
        context = super(Month72View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month72ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth72ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth72Report.objects.filter(month_72_report=report),
            'project_images': RelevantPictures72.objects.filter(grant_report=report),
            'month':'month72',
            'accept_url':'accept_twelveth_report'
        })
        print(context)

        return context


class Month78View(LoginRequiredMixin, DetailView):
    model = Month78Report
    context_object_name = "report"
    template_name = "month78.html"

    def get_context_data(self, **kwargs):
        context = super(Month78View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month78ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth78ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth78Report.objects.filter(month_78_report=report),
            'project_images': RelevantPictures78.objects.filter(grant_report=report),
            'month':'month78',
            'accept_url':'accept_thirteenth_report'
        })
        print(context)

        return context


class Month84View(LoginRequiredMixin, DetailView):
    model = Month84Report
    context_object_name = "report"
    template_name = "month84.html"

    def get_context_data(self, **kwargs):
        context = super(Month84View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month84ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth84ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth84Report.objects.filter(month_84_report=report),
            'project_images': RelevantPictures84.objects.filter(grant_report=report),
            'month':'month84',
            'accept_url':'accept_fourteenth_report'
        })
        print(context)

        return context


class Month90View(LoginRequiredMixin, DetailView):
    model = Month90Report
    context_object_name = "report"
    template_name = "month90.html"

    def get_context_data(self, **kwargs):
        context = super(Month90View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month90ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth90ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth90Report.objects.filter(month_90_report=report),
            'project_images': RelevantPictures90.objects.filter(grant_report=report),
            'month':'month90',
            'accept_url':'accept_fifteenth_report'
        })
        print(context)

        return context


class Month96View(LoginRequiredMixin, DetailView):
    model = Month96Report
    context_object_name = "report"
    template_name = "month96.html"

    def get_context_data(self, **kwargs):
        context = super(Month96View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month96ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth96ReportFormSet(prefix='student_report_set',
                                                                  instance=self.get_object()),
            "student_reports": Studentmonth96Report.objects.filter(month_96_report=report),
            'project_images': RelevantPictures96.objects.filter(grant_report=report),
            'month':'month96',
            'accept_url':'accept_sixteenth_report'
        })
        print(context)

        return context


class Month102View(LoginRequiredMixin, DetailView):
    model = Month102Report
    context_object_name = "report"
    template_name = "month102.html"

    def get_context_data(self, **kwargs):
        context = super(Month102View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month102ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth102ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth102Report.objects.filter(month_102_report=report),
            'project_images': RelevantPictures102.objects.filter(grant_report=report),
            'month':'month102',
            'accept_url':'accept_seventeenth_report'
        })
        print(context)

        return context


class Month108View(LoginRequiredMixin, DetailView):
    model = Month108Report
    context_object_name = "report"
    template_name = "month108.html"

    def get_context_data(self, **kwargs):
        context = super(Month108View, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month108ReportForm(instance=self.get_object()),
            "student_report_formset": Studentmonth108ReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports": Studentmonth108Report.objects.filter(month_108_report=report),
            'project_images': RelevantPictures108.objects.filter(grant_report=report),
            'month':'month108',
            'accept_url':'accept_eighteenth_report'
        })
        print(context)

        return context


class LastReportView(LoginRequiredMixin, DetailView):
    model = LastReport
    context_object_name = "report"
    template_name = "last_report.html"

    def get_context_data(self, **kwargs):
        context = super(LastReportView, self).get_context_data(**kwargs)
        report = context["report"]
        context.update({
            "comments": report.get_comments(),
            "form": Month30ReportForm(instance=self.get_object()),
            "student_report_formset": LastStudentReportFormSet(prefix='student_report_set', instance=self.get_object()),
            "student_reports":LastStudentReport.objects.filter(month_30_report=report),
            'pi_publications' : PIPublications.objects.filter(grant_report=report),
            'student_publications':StudentPublication.objects.filter(grant_report =report),
            'technologies': Technology.objects.filter(grant_report =report)
        })
        print(context)

        return context


class GrantsReportView(LoginRequiredMixin, TemplateView):
    model = TempReport
    context_object_name = "reports_list"
    template_name = "grants_reports.html"

    def get_queryset(self):
        queryset = self.model.objects.order_by('month','last_submitted')
        
        return queryset.distinct()

    def get_grant_manager_context(self):
        context = {}
        context['grant_reports']=self.get_queryset()
        
    
        return context

    def get_context_data(self, **kwargs):
        context = super(GrantsReportView, self).get_context_data(**kwargs)
        if has_group(self.request.user, 'Grants Managers') or self.request.user.is_superuser:
            return self.get_grant_manager_context()

        return context
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateGrantApprovalView(LoginRequiredMixin, CreateView):
    model = Grant
    form_class = GrantApprovalForm
    template_name = "create_grant_approval.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateGrantApprovalView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateGrantApprovalView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            log.error(form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Grant
        grantobject = form.save(commit=False)
        application = Grantapplication.objects.get(pk=self.kwargs['pk'])
        grantobject.grant_application = application
        grantobject.title = application.proposal
        grantobject.summary = application.proposal_title
        try:
            grantobject.theme = application.call.proposal_theme.name
        except:
            grantobject.theme =None
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        reporting_period = form.cleaned_data['reporting_period']
        days = end_date - start_date
        actual_start_date = datetime.datetime.strptime(str(start_date),'%Y-%m-%d')
        actual_end_date = datetime.datetime.strptime(str(end_date),'%Y-%m-%d')
        delta =relativedelta.relativedelta(actual_end_date,actual_start_date)
        no_of_reports = int((delta.years*12 + delta.months)/reporting_period)
        grantobject.duration = days.days
        grantobject.pi = application.user
        grantobject.report_number = no_of_reports
        grantobject.approval_status = 'approved'
        current_year = str(date.today().year)
        last_grant = Grant.objects.latest('id')
        generated_grant_number = 0
        #getting last call year
        last_grant_year = last_grant.grant_year
        last_inserted_generated_number = last_grant.generated_number
        if(last_grant_year == str(date.today().year)):
            generated_grant_number = last_inserted_generated_number + 1
        else:
            generated_grant_number=0+1
        grantobject.grant_id = 'RU/'+ str(application.call.grant_type) + "/"+ current_year +'/'+'G/'+ str(format(int(generated_grant_number),"04"))
        grantobject.value_chain = application.call.commodity_focus.name
        grantobject.created_by = self.request.user
        # change applicant to PI
        pigroup= Group.objects.get(name='PIs')
        application.user.groups.clear()
        application.user.groups.add(pigroup)
        application.selected_for_funding = True
        application.state='selected_for_funding'
        application.save()
        grantobject.save()
        form.save_m2m()
        # sending email to the selected pi 

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grant Application'
        message = render_to_string('grant_award_email.html', {
                'user': application.user,
                'domain': current_site.domain,
                'application': application
                
        })
        email = EmailMessage(mail_subject, message, to=[application.user.business_email],from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        email.send()
        if self.request.POST.get("savenewform"):
            return redirect("grants:new_account")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grants:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant was created successfully.')
        return redirect("grants:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateGrantApprovalView, self).get_context_data(**kwargs)
        context["grant_form"] = context["form"]
        return context
    def get_initial(self, *args, **kwargs):
        initial = super(CreateGrantApprovalView, self).get_initial(**kwargs)
       
        application = Grantapplication.objects.get(pk=self.kwargs['pk'])
        initial.update({
            'budget': application.total_budget,
           
        })
        return initial