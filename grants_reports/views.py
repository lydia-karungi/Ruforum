from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from navutils import MenuMixin
from grants.models import Grant
from common.models import User
from .models import FirstReport, RelevantPictures12, RelevantPictures18, RelevantPictures24, RelevantPictures30, \
    Studentmonth36Report, RelevantPictures36, RelevantPictures42, Studentmonth42Report, Studentmonth48Report, \
    RelevantPictures48, Studentmonth54Report, RelevantPictures54, RelevantPictures60, Studentmonth60Report, \
    RelevantPictures66, Studentmonth66Report, Studentmonth72Report, RelevantPictures72, RelevantPictures78, \
    Studentmonth78Report, RelevantPictures84, Studentmonth84Report, Studentmonth90Report, RelevantPictures90, \
    RelevantPictures96, Studentmonth96Report, Studentmonth102Report, RelevantPictures102, Studentmonth108Report, \
    RelevantPictures108
from django.http import JsonResponse
from django.forms import formset_factory
from .forms import (Month6ReportForm, Studentmonth6ReportForm, Month12ReportForm, Studentmonth12ReportForm,

                    Month18ReportForm, Month24ReportForm, LastReportForm,
                    Studentmonth18ReportForm, Month30ReportForm, LastStudentReportFormSet, LastStudentReportForm,
                    Studentmonth30ReportForm, Studentmonth12ReportFormSet, Studentmonth6ReportFormSet,
                    Studentmonth18ReportFormSet, Studentmonth24ReportForm, Studentmonth24ReportFormSet,
                    Studentmonth30ReportFormSet, Month36ReportForm, Month42ReportForm,
                    Month48ReportForm,Linkage18FormSet,
                    Month54ReportForm, Month60ReportForm, Month66ReportForm,
                    Month72ReportForm, Month78ReportForm, Month84ReportForm, Month90ReportForm, Month96ReportForm,
                    Month102ReportForm, Month108ReportForm, TechnologyFormSet, StudentPublicationFormSet,
                    PIPublicationFormSet, RelevantPictures12Form, RelevantPictures18Form, RelevantPictures24Form,
                    RelevantPictures30Form, Studentmonth36ReportFormSet, LastStudentReportFormSet,
                    RelevantPictures12FormSet, RelevantPictures18FormSet, RelevantPictures24FormSet,
                    Studentmonth36ReportForm, RelevantPictures30FormSet, RelevantPictures36Form,
                    RelevantPictures36FormSet, RelevantPictures42Form, Studentmonth42ReportForm,
                    Studentmonth42ReportFormSet, RelevantPictures42FormSet, Studentmonth48ReportForm,
                    RelevantPictures48Form, Studentmonth48ReportFormSet, RelevantPictures48FormSet,
                    Studentmonth54ReportFormSet, Studentmonth54ReportForm, RelevantPictures54Form,
                    RelevantPictures54FormSet, RelevantPictures60Form, Studentmonth60ReportForm,
                    Studentmonth60ReportFormSet, RelevantPictures60FormSet, RelevantPictures66Form,
                    Studentmonth66ReportForm, Studentmonth66ReportFormSet, RelevantPictures66FormSet,
                    Studentmonth72ReportFormSet, Studentmonth72ReportForm, RelevantPictures72Form,
                    RelevantPictures72FormSet, RelevantPictures78Form, Studentmonth78ReportForm,
                    Studentmonth78ReportFormSet, RelevantPictures78FormSet, RelevantPictures84Form,
                    Studentmonth84ReportFormSet, Studentmonth84ReportForm, Studentmonth90ReportForm,
                    RelevantPictures90Form, Studentmonth90ReportFormSet, RelevantPictures90FormSet,
                    RelevantPictures96Form, Studentmonth96ReportForm, Studentmonth96ReportFormSet,
                    RelevantPictures96FormSet, Studentmonth102ReportForm, Studentmonth102ReportFormSet,
                    RelevantPictures102Form, RelevantPictures102FormSet, Studentmonth108ReportForm,
                    RelevantPictures108FormSet, RelevantPictures108Form, Studentmonth108ReportFormSet,
                    RelevantPictures84FormSet, Linkage12FormSet,CourseFormSet, EditMonth6ReportForm
                    ,Linkage18Form,Linkage24FormSet,Linkage30FormSet,Linkage36FormSet,Linkage42FormSet
                    ,Linkage48FormSet,Linkage54FormSet,Linkage60FormSet,Linkage66FormSet,Linkage72FormSet,
                    Linkage78FormSet,Linkage84FormSet,Linkage90FormSet,Linkage96FormSet,Linkage102FormSet,
                    Linkage108FormSet)

from django.forms.models import inlineformset_factory
from .models import (FirstStudentReport, FirstReport, Month12Report, Month18Report, Month24Report, Month30Report,
                     LastReport, Studentmonth12Report, Studentmonth18Report,
                     Studentmonth24Report, Studentmonth30Report, LastStudentReport, Month36Report, Month42Report,
                     Month48Report, Month54Report, Month60Report, Month66Report, Month72Report, Month78Report,
                     Month84Report,
                     Month90Report, Month96Report, Month102Report, Month108Report, )
from django.utils.datetime_safe import datetime
from dateutil.relativedelta import relativedelta
from .serializers import ReportSerializer
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ReportSerializer
from rest_framework import filters
from .models import TempReport
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from smtplib import SMTPException

# Create your views here.


class PIreportsListView(MenuMixin, LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "pi_reports_list"
    template_name = "my_pi_reports.html"
    current_menu_item = 'my_pi_reports'

    def get_context_data(self, **kwargs):
        context = super(PIreportsListView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        periods = []
        if self.object.reporting_period == 3: periods = Grant.PERIOD_CHOICES[:self.object.report_number]
        if self.object.reporting_period == 6: periods = Grant.PERIOD_CHOICES6[:self.object.report_number]
        statuses = []

        report_data = []
        for (n, period) in enumerate(periods):

            try:

                month6grrantreport = FirstReport.objects.filter(grant=self.object)
                if n == 0 and month6grrantreport.exists():
                    statuses.append("Submitted")
                    print(self.object.report_number)
                elif n == 0 and not month6grrantreport:
                    statuses.append("Not Submitted")

                month12grrantreport = Month12Report.objects.filter(grant=self.object)
                if n == 1 and month12grrantreport:
                    statuses.append("Submitted")
                    print(month12grrantreport)
                elif n == 1 and not month12grrantreport:
                    statuses.append("Not Submitted")

                month18grrantreport = Month18Report.objects.filter(grant=self.object)
                if n == 2 and month18grrantreport:
                    statuses.append("Submitted")
                    print(month18grrantreport)
                elif n == 2 and not month18grrantreport:
                    statuses.append("Not Submitted")

                month24grrantreport = Month24Report.objects.filter(grant=self.object)
                if n == 3 and month24grrantreport:
                    statuses.append("Submitted")
                    print(month24grrantreport)
                elif n == 3 and not month24grrantreport:
                    statuses.append("Not Submitted")

                month30grrantreport = Month30Report.objects.filter(grant=self.object)
                if n == 4 and month30grrantreport:
                    statuses.append("Submitted")
                    print(month30grrantreport)
                elif n == 4 and not month30grrantreport:
                    statuses.append("Not Submitted")

                month36grrantreport = Month36Report.objects.filter(grant=self.object)
                if n == 5 and month36grrantreport:
                    statuses.append("Submitted")
                    print(month36grrantreport)
                elif n == 5 and not month36grrantreport:
                    statuses.append("Not Submitted")

                month42grrantreport = Month42Report.objects.filter(grant=self.object)
                if n == 6 and month42grrantreport:
                    statuses.append("Submitted")
                    print(month42grrantreport)
                elif n == 6 and not month42grrantreport:
                    statuses.append("Not Submitted")

                month48grrantreport = Month48Report.objects.filter(grant=self.object)
                if n == 7 and month48grrantreport:
                    statuses.append("Submitted")
                    print(month48grrantreport)
                elif n == 7 and not month48grrantreport:
                    statuses.append("Not Submitted")

                lastgrrantreport = LastReport.objects.filter(grant=self.object)
                if n == 8 and lastgrrantreport:
                    statuses.append("Submitted")
                    print(lastgrrantreport)
                elif n == 8 and not lastgrrantreport:
                    statuses.append("Not Submitted")

            except Grant.DoesNotExist:

                report = None
            data = {
                'period': period[0],
                'description': period[1],
            }
            report_data.append(data)

        context['report_data'] = report_data
        context['grant'] = self.object
        context['statuses'] = statuses
        print(periods)
        return context


class CreatePireportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_6month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePireportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        ids = self.object.students.all()
        print(ids)
        context["form"] = Month6ReportForm
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3)
            month = 3
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6)
            month = 6
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['report_due_date'] = report_due_date
        context['month'] = month
        Studentmonth6ReportFormSet = inlineformset_factory(FirstReport, FirstStudentReport,
                                                           form=Studentmonth6ReportForm, min_num=stud_num, extra=0,
                                                           can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth6ReportFormSet(prefix='student_set')
        grantrecord = context["grant"]

        return context


class SavePireportView(LoginRequiredMixin, CreateView):
    model = FirstReport
    form_class = Month6ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePireportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePireportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth6ReportFormSet(request.POST, request.FILES, prefix='student_set')
        formsets_valid = (
            self.student_form.is_valid() 
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print('--------------------')
           
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        student_object = self.student_form
        student_object.instance = reportobject
        student_object.save(commit = False)
        student_object.save()
        form.save_m2m()
        # send to all grants managers an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 
        

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {'error': True, 'errors': form.errors.as_json(), 'student_errors': self.student_form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePireportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth6ReportFormSet(prefix='student_set')
       
        return context



class UpdateFirstPIView(LoginRequiredMixin, UpdateView):
    model = FirstReport
    form_class = EditMonth6ReportForm
    template_name = "edit_6month.html"
  
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateFirstPIView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateFirstPIView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth6ReportFormSet(request.POST, request.FILES, prefix='student_set', instance=self.object)
        formsets_valid = (
            self.student_form.is_valid() 
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print('--------------------')

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        student_object = self.student_form
        student_object.instance = reportobject
        student_object.save(commit = False)
        student_object.save()
        form.save_m2m()
        

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {'error': True, 'errors': form.errors.as_json(), 'student_errors': self.student_form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form)
        )

    def get_context_data(self, **kwargs):
        context = super(UpdateFirstPIView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context["grant"] = self.object.grant
        context['student_formset'] = context.get('student_form') or Studentmonth6ReportFormSet(instance=self.object, prefix='student_set')
        return context


# create pi twelve month report
class CreatePi12MonthreportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_12month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi12MonthreportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month12ReportForm
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 2)
            month = 6

        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 2)
            month = 12
        
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['report_due_date'] = report_due_date
        context['month'] = month
        RelevantPictures12FormSet = inlineformset_factory(Month12Report, RelevantPictures12,
                                                          form=RelevantPictures12Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures12FormSet(prefix='picture_set')
        Studentmonth12ReportFormSet = inlineformset_factory(Month12Report, Studentmonth12Report,
                                                            form=Studentmonth12ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth12ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage12FormSet(prefix='linkage_set')

        return context


class SavePi12MonthreportView(LoginRequiredMixin, CreateView):
    model = Month12Report
    form_class = Month12ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi12MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi12MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth12ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures12FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage12FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi12MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth12ReportFormSet(prefix='student_set')
        #context['student_formset'] = context.get('student_form') or Studentmonth12ReportFormSet(prefix='student_set')
        return context


# update 12 month report
class Edit12MonthreportView(LoginRequiredMixin, UpdateView):
    model = Month12Report
    form_class = Month12ReportForm
    template_name = "edit_pi_12month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edit12MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edit12MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth12ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures12FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage12FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edit12MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures12FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth12ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage12FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context



# create pi eighteen month report
class CreatePi18MonthreportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_18month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi18MonthreportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month18ReportForm
        context['previous_report'] = Month12Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 3)
            month = 9
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 3)
            month = 18
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures18FormSet = inlineformset_factory(Month18Report, RelevantPictures18,
                                                          form=RelevantPictures18Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures18FormSet(prefix='picture_set')
        Studentmonth18ReportFormSet = inlineformset_factory(Month18Report, Studentmonth18Report,
                                                            form=Studentmonth18ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth18ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage18FormSet(prefix='linkage_set')
        

        return context


class SavePi18MonthreportView(LoginRequiredMixin, CreateView):
    model = Month18Report
    form_class = Month18ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi18MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi18MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth18ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.linkage_form = Linkage18FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
            self.student_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and self.student_form.is_valid() and self.linkage_form.is_valid()
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form,linkage_form =self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi18MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth18ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage18FormSet(prefix='linkage_set')
        
        return context


# update 18 month report
class Edit18MonthreportView(LoginRequiredMixin, UpdateView):
    model = Month18Report
    form_class = Month18ReportForm
    template_name = "edit_pi_18month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edit18MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edit18MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth18ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures18FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage18FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edit18MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures18FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth18ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage18FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context

# create pi twenty four month report
class CreatePi24MonthreportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_24month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi24MonthreportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month24ReportForm
        context['previous_report'] = Month18Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 4)
            month = 12
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 4)
            month = 24
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures24FormSet = inlineformset_factory(Month24Report, RelevantPictures24,
                                                          form=RelevantPictures24Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures24FormSet(prefix='picture_set')
        Studentmonth24ReportFormSet = inlineformset_factory(Month24Report, Studentmonth24Report,
                                                            form=Studentmonth24ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth24ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage24FormSet(prefix='linkage_set')

        return context


class SavePi24MonthreportView(LoginRequiredMixin, CreateView):
    model = Month24Report
    form_class = Month24ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi24MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi24MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth24ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures24FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage24FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form, linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi24MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth24ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage24FormSet(prefix='linkage_set')
        return context


# update 24 month report
class Edit24MonthreportView(LoginRequiredMixin, UpdateView):
    model = Month24Report
    form_class = Month24ReportForm
    template_name = "edit_pi_24month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edit24MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edit24MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth24ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures24FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage24FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edit24MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures24FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth24ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage24FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context

# create pi thirty  month report
class CreatePi30MonthreportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_30month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi30MonthreportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month30ReportForm
        context['previous_report'] = Month24Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 5)
            month = 15
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 5)
            month = 30
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures30FormSet = inlineformset_factory(Month30Report, RelevantPictures30,
                                                          form=RelevantPictures30Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures30FormSet(prefix='picture_set')
        Studentmonth30ReportFormSet = inlineformset_factory(Month30Report, Studentmonth30Report,
                                                            form=Studentmonth30ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth30ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage30FormSet(prefix='linkage_set')
        return context


class SavePi30MonthreportView(LoginRequiredMixin, CreateView):
    model = Month30Report
    form_class = Month30ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi30MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi30MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth30ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures30FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage30FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi30MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures30FormSet(prefix='picture_set')
        context['student_formset'] = context.get('student_form') or Studentmonth30ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage30FormSet(prefix='linkage_set')
        return context


# update 30 month report
class Edite30MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month30Report
    form_class = Month30ReportForm
    template_name = "edit_pi_30month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite30MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite30MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth30ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures30FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage30FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite30MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures30FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth30ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage30FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


class CreatePiLastreportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "last_pi_grant_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePiLastreportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = LastReportForm
        LastStudentReportFormSet = inlineformset_factory(LastReport, LastStudentReport,
                                                         form=LastStudentReportForm, min_num=stud_num, extra=0,
                                                         can_delete=False)
        context['student_formset'] = context.get('student_form') or LastStudentReportFormSet(prefix='student_set')
        context['technology_formset'] = context.get('technology') or TechnologyFormSet(prefix='technology_set')
        context['student_publication_formset'] = context.get('student_publication_form') or \
                                                 StudentPublicationFormSet(prefix='student_publication_set')
        context['pi_publication_formset'] = context.get('pi_publication_form') or PIPublicationFormSet(
            prefix='pi_publication_set')

        return context


# Pi last report
class SavePiLastreportView(LoginRequiredMixin, CreateView):
    model = LastReport
    form_class = LastReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePiLastreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePiLastreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = LastStudentReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.technology = TechnologyFormSet(request.POST, request.FILES, prefix='technology_set')
        self.pi_publication_form = PIPublicationFormSet(request.POST, request.FILES, prefix="pi_publication_set")
        self.student_publication_form = StudentPublicationFormSet(request.POST, request.FILES,
                                                                  prefix="student_publication_set")
        formsets_valid = (
                self.student_form.is_valid() and self.technology.is_valid() and self.pi_publication_form.is_valid()
                and self.student_publication_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.technology.errors)
            print(self.student_publication_form.errors)
            print(self.pi_publication_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        report_object = form.save(commit=False)
        report_object.started = 1
        report_object.last_submitted = datetime.now()
        report_object.save()
        self.student_form.instance = report_object
        self.student_form.save()
        self.technology.instance = report_object
        self.technology.save()
        self.pi_publication_form.instance = report_object
        self.pi_publication_form.save()
        self.student_publication_form.instance = report_object
        self.student_publication_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, student_form=self.student_form, technology=self.technology)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePiLastreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or LastStudentReportFormSet(prefix='student_set')
        context['technology_formset'] = context.get('technology') or TechnologyFormSet(prefix='technology_set')
        return context


#edit last report
class EditPiLastreportView(LoginRequiredMixin, UpdateView):
    model = LastReport
    form_class = LastReportForm
    template_name = "edit_last_pi_grant_report.html"
   

    def dispatch(self, request, *args, **kwargs):
        return super(EditPiLastreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditPiLastreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.student_form = LastStudentReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.technology = TechnologyFormSet(request.POST, request.FILES, prefix='technology_set',instance=self.object)
        self.pi_publication_form = PIPublicationFormSet(request.POST, request.FILES, prefix="pi_publication_set",instance=self.object)
        self.student_publication_form = StudentPublicationFormSet(request.POST, request.FILES,
                                                                  prefix="student_publication_set",instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.technology.is_valid() and self.pi_publication_form.is_valid()
                and self.student_publication_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.technology.errors)
            print(self.student_publication_form.errors)
            print(self.pi_publication_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        report_object = form.save(commit=False)
        report_object.started = 1
        report_object.last_submitted = datetime.now()
        report_object.save()
        self.student_form.instance = report_object
        self.student_form.save()
        self.technology.instance = report_object
        self.technology.save()
        self.pi_publication_form.instance = report_object
        self.pi_publication_form.save()
        self.student_publication_form.instance = report_object
        self.student_publication_form.save()
        form.save_m2m()

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, student_form=self.student_form, technology=self.technology)
        )

    def get_context_data(self, **kwargs):
        context = super(EditPiLastreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or LastStudentReportFormSet(prefix='student_set',instance=self.object)
        context['technology_formset'] = context.get('technology') or TechnologyFormSet(prefix='technology_set',instance=self.object)
        context['student_publication_formset'] = context.get('student_publication_form') or \
                                                 StudentPublicationFormSet(prefix='student_publication_set', instance=self.object)
        context['pi_publication_formset'] = context.get('pi_publication_form') or PIPublicationFormSet(
            prefix='pi_publication_set', instance=self.object)
        return context

'''Create Student's report '''


class CreatePi36MonthreportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_36month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi36MonthreportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month36ReportForm
        context['previous_report'] = Month30Report.objects.filter(grant=self.object)
        context['url'] = 'grants_reports:save_thirty_six_month_report'
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 6)
            month = 18
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 6)
            month = 36
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures36FormSet = inlineformset_factory(Month36Report, RelevantPictures36,
                                                          form=RelevantPictures36Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures36FormSet(prefix='picture_set')
        Studentmonth36ReportFormSet = inlineformset_factory(Month36Report, Studentmonth36Report,
                                                            form=Studentmonth36ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth36ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage36FormSet(prefix='linkage_set')
        return context


class SavePi36MonthreportView(LoginRequiredMixin, CreateView):
    model = Month36Report
    form_class = Month36ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi36MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi36MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth36ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures36FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage36FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form, linkage_form= self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi36MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth36ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth36ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage36FormSet(prefix='linkage_set')
        return context

# update 36 month report
class Edite36MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month36Report
    form_class = Month36ReportForm
    template_name = "edit_pi_36month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite36MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite36MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth36ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures36FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage36FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite36MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures36FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth36ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage36FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 42 month grant report
class CreatePi42MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_42month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi42MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month42ReportForm
        context['previous_report'] = Month36Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 7)
            month = 21
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 7)
            month = 42
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures42FormSet = inlineformset_factory(Month42Report, RelevantPictures42,
                                                          form=RelevantPictures42Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures42FormSet(prefix='picture_set')
        Studentmonth42ReportFormSet = inlineformset_factory(Month42Report, Studentmonth42Report,
                                                            form=Studentmonth42ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth42ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage42FormSet(prefix='linkage_set')

        return context


class SavePi42MonthReportView(LoginRequiredMixin, CreateView):
    model = Month42Report
    form_class = Month42ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi42MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi42MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth42ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures42FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage42FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi42MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth42ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth42ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage42FormSet(prefix='linkage_set')
        return context

# update 42 month report
class Edite42MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month42Report
    form_class = Month42ReportForm
    template_name = "edit_pi_42month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite42MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite42MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth42ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures42FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage42FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite42MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures42FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth42ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage42FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context
 

# 48 month grant report
class CreatePi48MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_48month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi48MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month48ReportForm
        context['previous_report'] = Month42Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 8)
            month = 24
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 8)
            month = 48
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures48FormSet = inlineformset_factory(Month48Report, RelevantPictures48,
                                                          form=RelevantPictures48Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures48FormSet(prefix='picture_set')
        Studentmonth48ReportFormSet = inlineformset_factory(Month48Report, Studentmonth48Report,
                                                            form=Studentmonth48ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth48ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage48FormSet(prefix='linkage_set')

        return context


class SavePi48MonthReportView(LoginRequiredMixin, CreateView):
    model = Month48Report
    form_class = Month48ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi48MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi48MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth48ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures48FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage48FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form, linkage_form = self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi48MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth48ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth48ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage48FormSet(prefix='linkage_set')
        return context

# update 48 month report
class Edite48MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month48Report
    form_class = Month48ReportForm
    template_name = "edit_pi_48month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite48MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite48MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth48ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures48FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage48FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite48MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures48FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth48ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage48FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 54 month grant report
class CreatePi54MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_54month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi54MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month54ReportForm
        context['previous_report'] = Month48Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 9)
            month = 27
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 9)
            month = 54
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures54FormSet = inlineformset_factory(Month54Report, RelevantPictures54,
                                                          form=RelevantPictures54Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures54FormSet(prefix='picture_set')
        Studentmonth54ReportFormSet = inlineformset_factory(Month54Report, Studentmonth54Report,
                                                            form=Studentmonth54ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth54ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage54FormSet(prefix='linkage_set')

        return context


class SavePi54MonthReportView(LoginRequiredMixin, CreateView):
    model = Month54Report
    form_class = Month54ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi54MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi54MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth54ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures54FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage54FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form, linkage_form = self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi54MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth54ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth54ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage54FormSet(prefix='linkage_set')
        return context

# update 54 month report
class Edite54MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month54Report
    form_class = Month54ReportForm
    template_name = "edit_pi_54month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite54MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite54MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth54ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures54FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage54FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite54MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures54FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth54ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage54FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 60 month grant report
class CreatePi60MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_60month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi60MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month60ReportForm
        context['previous_report'] = Month54Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 10)
            month = 30
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 10)
            month = 66
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures60FormSet = inlineformset_factory(Month60Report, RelevantPictures60,
                                                          form=RelevantPictures60Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures60FormSet(prefix='picture_set')
        Studentmonth60ReportFormSet = inlineformset_factory(Month60Report, Studentmonth60Report,
                                                            form=Studentmonth60ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth60ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage60FormSet(prefix='linkage_set')

        return context


class SavePi60MonthReportView(LoginRequiredMixin, CreateView):
    model = Month60Report
    form_class = Month60ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi60MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi60MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth60ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures60FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage60FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi60MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth60ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth60ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage60FormSet(prefix='linkage_set')
        return context

# update 60 month report
class Edite60MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month60Report
    form_class = Month60ReportForm
    template_name = "edit_pi_60month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite60MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite60MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth60ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures60FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage60FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite60MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures60FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth60ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage60FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 66 month grant report
class CreatePi66MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_66month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi66MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month66ReportForm
        context['previous_report'] = Month60Report.objects.filter(grant=self.object)
        context['url'] = 'grants_reports:save_thirty_six_month_report'
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 11)
            month = 33
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 11)
            month = 66
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures66FormSet = inlineformset_factory(Month66Report, RelevantPictures66,
                                                          form=RelevantPictures66Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures66FormSet(prefix='picture_set')
        Studentmonth66ReportFormSet = inlineformset_factory(Month66Report, Studentmonth66Report,
                                                            form=Studentmonth66ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth66ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage66FormSet(prefix='linkage_set')

        return context


class SavePi66MonthReportView(LoginRequiredMixin, CreateView):
    model = Month66Report
    form_class = Month66ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi66MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi66MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth66ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures66FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage66FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi66MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth66ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth66ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage66FormSet(prefix='linkage_set')
        return context


# update 66 month report
class Edite66MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month66Report
    form_class = Month66ReportForm
    template_name = "edit_pi_66month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite66MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite66MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth66ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures66FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage66FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite66MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures66FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth66ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage66FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 72 grant report
class CreatePi72MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_72month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi72MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month72ReportForm
        context['previous_report'] = Month66Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 12)
            month = 36
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 12)
            month = 72
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures72FormSet = inlineformset_factory(Month72Report, RelevantPictures72,
                                                          form=RelevantPictures72Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures72FormSet(prefix='picture_set')
        Studentmonth72ReportFormSet = inlineformset_factory(Month72Report, Studentmonth72Report,
                                                            form=Studentmonth72ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth72ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage72FormSet(prefix='linkage_set')

        return context


class SavePi72MonthReportView(LoginRequiredMixin, CreateView):
    model = Month72Report
    form_class = Month72ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi72MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi72MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth72ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures72FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage72FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and  self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        
        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi72MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth72ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth72ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage72FormSet(prefix='linkage_set')
        return context

# update 72 month report
class Edite72MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month72Report
    form_class = Month72ReportForm
    template_name = "edit_pi_72month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite72MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite72MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth72ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures72FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage72FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite72MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures72FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth72ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage72FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 78 month grant report
class CreatePi78MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_78month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi78MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month78ReportForm
        context['previous_report'] = Month72Report.objects.filter(grant=self.object)
        context['url'] = 'grants_reports:save_thirty_six_month_report'
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 13)
            month = 39
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 13)
            month = 78
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures78FormSet = inlineformset_factory(Month78Report, RelevantPictures78,
                                                          form=RelevantPictures78Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures78FormSet(prefix='picture_set')
        Studentmonth78ReportFormSet = inlineformset_factory(Month78Report, Studentmonth78Report,
                                                            form=Studentmonth78ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth78ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage78FormSet(prefix='linkage_set')

        return context


class SavePi78MonthReportView(LoginRequiredMixin, CreateView):
    model = Month78Report
    form_class = Month78ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi78MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi78MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth78ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures78FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage78FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

        # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi78MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth78ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth78ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage78FormSet(prefix='linkage_set')
        return context

# update 78 month report
class Edite78MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month78Report
    form_class = Month78ReportForm
    template_name = "edit_pi_78month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite78MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite78MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth78ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures78FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage78FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite78MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures78FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth78ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage78FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 84 grant report
class CreatePi84MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_84month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi84MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month36ReportForm
        context['previous_report'] = Month78Report.objects.filter(grant=self.object)
        context['url'] = 'grants_reports:save_thirty_six_month_report'
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 14)
            month = 42
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 14)
            month = 84
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures84FormSet = inlineformset_factory(Month84Report, RelevantPictures84,
                                                          form=RelevantPictures84Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures84FormSet(prefix='picture_set')
        Studentmonth84ReportFormSet = inlineformset_factory(Month84Report, Studentmonth84Report,
                                                            form=Studentmonth84ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth84ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage84FormSet(prefix='linkage_set')
        return context


class SavePi84MonthReportView(LoginRequiredMixin, CreateView):
    model = Month84Report
    form_class = Month84ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi84MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi84MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth84ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures84FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage84FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

          # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi84MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth84ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth84ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage84FormSet(prefix='linkage_set')
        return context

# update 84 month report
class Edite84MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month84Report
    form_class = Month84ReportForm
    template_name = "edit_pi_84month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite84MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite84MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth84ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures84FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage84FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite84MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures84FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth84ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage84FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 90 month grant report
class CreatePi90MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_90month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi90MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month90ReportForm
        context['previous_report'] = Month84Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 15)
            month = 45
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 15)
            month = 90
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures90FormSet = inlineformset_factory(Month90Report, RelevantPictures90,
                                                          form=RelevantPictures90Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures90FormSet(prefix='picture_set')
        Studentmonth90ReportFormSet = inlineformset_factory(Month90Report, Studentmonth90Report,
                                                            form=Studentmonth90ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth90ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage90FormSet(prefix='linkage_set')

        return context


class SavePi90MonthReportView(LoginRequiredMixin, CreateView):
    model = Month90Report
    form_class = Month90ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi90MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi90MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth90ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures90FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage90FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

          # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 


        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi90MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth90ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth90ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage90FormSet(prefix='linkage_set')
        return context

# update 90 month report
class Edite90MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month90Report
    form_class = Month90ReportForm
    template_name = "edit_pi_90month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite90MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite90MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth90ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures90FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage90FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite90MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures90FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth90ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage90FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context

# 96 grant report
class CreatePi96MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_96month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi96MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month96ReportForm
        context['previous_report'] = Month90Report.objects.filter(grant=self.object)
        context['url'] = 'grants_reports:save_thirty_six_month_report'
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 16)
            month = 48
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 16)
            month = 96
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures96FormSet = inlineformset_factory(Month96Report, RelevantPictures96,
                                                          form=RelevantPictures96Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures96FormSet(prefix='picture_set')
        Studentmonth96ReportFormSet = inlineformset_factory(Month96Report, Studentmonth96Report,
                                                            form=Studentmonth96ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth96ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage96FormSet(prefix='linkage_set')

        return context


class SavePi96MonthReportView(LoginRequiredMixin, CreateView):
    model = Month96Report
    form_class = Month96ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi96MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi96MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth96ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures96FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage96FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

          # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi96MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth96ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth96ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage96FormSet(prefix='linkage_set')
        return context

# update 96 month report
class Edite96MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month96Report
    form_class = Month96ReportForm
    template_name = "edit_pi_96month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite96MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite96MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth96ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures96FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage96FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite96MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures96FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth96ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage96FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 102 grant report
class CreatePi102MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_102month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi102MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month102ReportForm
        context['previous_report'] = Month96Report.objects.filter(grant=self.object)
        context['url'] = 'grants_reports:save_thirty_six_month_report'
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 17)
            month = 51
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 17)
            month = 102
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures102FormSet = inlineformset_factory(Month102Report, RelevantPictures102,
                                                          form=RelevantPictures102Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures102FormSet(prefix='picture_set')
        Studentmonth102ReportFormSet = inlineformset_factory(Month102Report, Studentmonth102Report,
                                                            form=Studentmonth102ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth102ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage102FormSet(prefix='linkage_set')

        return context


class SavePi102MonthReportView(LoginRequiredMixin, CreateView):
    model = Month102Report
    form_class = Month102ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi102MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi102MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth102ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures102FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage102FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()

          # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi102MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth102ReportFormSet(prefix='student_set')
        context['student_formset'] = context.get('student_form') or Studentmonth102ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage102FormSet(prefix='linkage_set')
        return context

# update 102 month report
class Edite102MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month102Report
    form_class = Month102ReportForm
    template_name = "edit_pi_102month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite102MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite102MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth102ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures102FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage102FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite102MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures102FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth102ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage102FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context


# 108 grant report
class CreatePi108MonthReportView(LoginRequiredMixin, DetailView):
    model = Grant
    context_object_name = "grantrecord"
    template_name = "create_pi_108month_report.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePi108MonthReportView, self).get_context_data(**kwargs)
        context["grant"] = self.object
        stud_num = self.object.students.all().count()
        context["form"] = Month108ReportForm
        context['previous_report'] = Month102Report.objects.filter(grant=self.object)
        reporting_period = self.object.reporting_period
        report_due_date = self.object.start_date
        if reporting_period == 3:
            report_due_date = self.object.start_date + relativedelta(months=3 * 18)
            month = 54
        elif reporting_period == 6:
            report_due_date = self.object.start_date + relativedelta(months=6 * 18)
            month = 108
        print(datetime.date(report_due_date))
        print(self.object.reporting_period)
        context['month'] = month
        context['report_due_date'] = report_due_date
        RelevantPictures108FormSet = inlineformset_factory(Month108Report, RelevantPictures108,
                                                          form=RelevantPictures108Form, extra=1, max_num=10,
                                                          can_delete=True)
        context['picture_formset'] = context.get('picture_form') or RelevantPictures108FormSet(prefix='picture_set')
        Studentmonth108ReportFormSet = inlineformset_factory(Month108Report, Studentmonth108Report,
                                                            form=Studentmonth108ReportForm, min_num=stud_num, extra=0,
                                                            can_delete=False)
        context['student_formset'] = context.get('student_form') or Studentmonth108ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage108FormSet(prefix='linkage_set')

        return context


class SavePi108MonthReportView(LoginRequiredMixin, CreateView):
    model = Month108Report
    form_class = Month108ReportForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(SavePi108MonthReportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SavePi108MonthReportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.student_form = Studentmonth108ReportFormSet(request.POST, request.FILES, prefix='student_set')
        self.picture_form = RelevantPictures108FormSet(request.POST, request.FILES, prefix='picture_set')
        self.linkage_form = Linkage108FormSet(request.POST, request.FILES, prefix='linkage_set')
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        report_object = form.save(commit=False)
        report_object.started = 1
        report_object.last_submitted = datetime.now()
        report_object.save()
        self.student_form.instance = report_object
        self.student_form.save()
        self.picture_form.instance = report_object
        self.picture_form.save()
        self.linkage_form.instance = report_object
        self.linkage_form.save()
        form.save_m2m()
          # send grants manager an email
        grants_managers = User.objects.filter(groups__name='Grants Managers')
        for user in grants_managers:
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grants Report  Submission'
            message = render_to_string('grants_report_submission_email.html', {
                'user': user,
                'domain': current_site.domain,
                'message': 'A PI Report has been submitted by '+ str(reportobject.grant.pi) + ' for your review.'
                })
            email = EmailMessage(mail_subject, message, to=[user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            try:
                email.send()
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

        # sending email to the pi
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Submission'
        message = render_to_string('grants_report_submission_email.html', {
            'user': reportobject.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Report has been submitted for review by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[reportobject.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form)
        )

    def get_context_data(self, **kwargs):
        context = super(SavePi108MonthReportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['student_formset'] = context.get('student_form') or Studentmonth108ReportFormSet(prefix='student_set')
        context['linkage_formset'] = context.get('linkage_form') or Linkage108FormSet(prefix='linkage_set')
        return context

# update 108 month report
class Edite108MonthreportView(LoginRequiredMixin, UpdateView):

    model = Month108Report
    form_class = Month108ReportForm
    template_name = "edit_pi_108month_report.html"


    def dispatch(self, request, *args, **kwargs):
        return super(Edite108MonthreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Edite108MonthreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object =  self.get_object()
        form = self.get_form()
        self.student_form = Studentmonth108ReportFormSet(request.POST, request.FILES, prefix='student_set',instance=self.object)
        self.picture_form = RelevantPictures108FormSet(request.POST, request.FILES, prefix='picture_set',instance=self.object)
        self.linkage_form = Linkage108FormSet(request.POST, request.FILES, prefix='linkage_set',instance=self.object)
        formsets_valid = (
                self.student_form.is_valid() and self.picture_form.is_valid() and self.linkage_form.is_valid()
        )
        forms_valid = (
                form.is_valid() and formsets_valid
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.student_form.errors)
            print(self.picture_form.errors)
            print(self.linkage_form.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        reportobject = form.save(commit=False)
        reportobject.started = 1
        reportobject.last_submitted = datetime.now()
        reportobject.save()
        self.student_form.instance = reportobject
        self.student_form.save()
        self.picture_form.instance = reportobject
        self.picture_form.save()
        self.linkage_form.instance = reportobject
        self.linkage_form.save()
        form.save_m2m()
       

        return redirect("PI:reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form,
                                  student_form=self.student_form, picture_form=self.picture_form,linkage_form=self.linkage_form)
        )

    def get_context_data(self, **kwargs):
        context = super(Edite108MonthreportView, self).get_context_data(**kwargs)
        context["grant_report_form"] = context["form"]
        context['picture_formset'] = context.get('picture_form') or RelevantPictures108FormSet(prefix='picture_set', instance=self.object)
        context['student_formset'] = context.get('student_form') or Studentmonth108ReportFormSet(prefix='student_set', instance=self.object)
        context['linkage_formset'] = context.get('linkage_form') or Linkage108FormSet(prefix='linkage_set', instance=self.object)
        context["grant"] = self.object
        return context

 #accept  PI first report
class AcceptFirstReportView(LoginRequiredMixin, DeleteView):
    model = FirstReport
    template_name = 'month6.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 


        return redirect('grants:grants_reports')

#accept  PI second report
class AcceptSecondReportView(LoginRequiredMixin, DeleteView):
    model = Month12Report
    template_name = 'month12.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptThirdReportView(LoginRequiredMixin, DeleteView):
    model = Month18Report
    template_name = 'month18.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')




#accept  PI third report
class AcceptFourthReportView(LoginRequiredMixin, DeleteView):
    model = Month24Report
    template_name = 'month24.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptFifthReportView(LoginRequiredMixin, DeleteView):
    model = Month30Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')



#accept  PI third report
class AcceptSixthReportView(LoginRequiredMixin, DeleteView):
    model = Month36Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptSeventhReportView(LoginRequiredMixin, DeleteView):
    model = Month42Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptEighthReportView(LoginRequiredMixin, DeleteView):
    model = Month48Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptNineththReportView(LoginRequiredMixin, DeleteView):
    model = Month54Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptTenthReportView(LoginRequiredMixin, DeleteView):
    model = Month60Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()

        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')

    
#accept  PI third report
class AcceptEleventhReportView(LoginRequiredMixin, DeleteView):
    model = Month66Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptTwelvethReportView(LoginRequiredMixin, DeleteView):
    model = Month72Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptThirteenthReportView(LoginRequiredMixin, DeleteView):
    model = Month78Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptFourteenthReportView(LoginRequiredMixin, DeleteView):
    model = Month84Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptFifteenthReportView(LoginRequiredMixin, DeleteView):
    model = Month90Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptSixteenthReportView(LoginRequiredMixin, DeleteView):
    model = Month96Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptSeventeenthReportView(LoginRequiredMixin, DeleteView):
    model = Month102Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')


#accept  PI third report
class AcceptEighteenthReportView(LoginRequiredMixin, DeleteView):
    model = Month108Report
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 
        return redirect('grants:grants_reports')

#accept  PI last report
class AcceptLastReportView(LoginRequiredMixin, DeleteView):
    model = LastReport
    template_name = 'month30.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accepted_on=datetime.now()
        self.object.accepted_by = self.request.user
        self.object.save()
        # send to the pi a message after accepting the report
        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grants Report  Accepted'
        message = render_to_string('grants_report_submission_email.html', {
            'user': self.object.grant.pi,
            'domain': current_site.domain,
            'message': 'Your Grant Report has been accepted by the grants manager.'
            })
        email = EmailMessage(mail_subject, message, to=[self.object.grant.pi.business_email],
                                 from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        try:
            email.send()
        except SMTPException as e:
            print('There was an error sending an email: ', e) 

        return redirect('grants:grants_reports')


# display grants reports viewset
class ReportsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = TempReport.objects.all().order_by('-id')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = '__all__'