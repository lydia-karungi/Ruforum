import datetime
import os
import tempfile
from datetime import date

import xlsxwriter
from dateutil import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Q, Sum, Avg
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, DeleteView)
from django_weasyprint import WeasyTemplateResponseMixin

from calls.models import Call
from contacts.models import User
from scholarships.models import (
    Scholarshipapplication, Scholarshipappreview, Referenceletter, Publication, Parent, Householdincomesource,
    Scholarship
)
from .forms import (
    ScholarshipForm, OtherForm, EducationFormSet, EmploymenthistoryFormSet,
    ReferenceletterFormSet, MastercardscholarshipapplicationForm,
    ScholarshipappreviewForm, SelectCallForm, ParentFormSet, MastercardeducationFormSet,
    HouseholdincomesourceFormSet, LeadershippositionFormSet, WorkexperienceFormSet, ResearchFormSet,
    ScholarshipReviewerForm, PublicationsFormSet, ScholarshipApprovalForm, ScholarshipApplicationRejectForm,
    ScholarshipValidatorForm, ScholarshipapplicationValidationForm,EditScholarshipForm
)
from .models import ResearchAndPublication
from .serializers import ScholarshipSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters


# Scholarships list
class ScholarshipsListView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "scholarships_list"
    template_name = "scholarships.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user.id).order_by('-id')
        state = ['submitted', 'draft', 'noncompliant']
        if self.request.user.has_perm(
                'scholarships.change_scholarshipapplication') or self.request.user.is_superuser or \
                self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(state='submitted').order_by('-id')

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('first_name')))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    Q(user__last_name__icontains=request_post.get('last_name')))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    Q(call__call_id__icontains=request_post.get('call_id')))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    Q(otherscholarshipapplication__programme_applied_for__contains=request_post.get('programme')))
            if request_post.get('type'):
                queryset = queryset.filter(
                    call__scholarship_type__icontains=request_post.get('type'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ScholarshipsListView, self).get_context_data(**kwargs)

        # open_scholarships = self.get_queryset().filter(status='open')
        # close_scholarships = self.get_queryset().filter(status='close')
        context["scholarships"] = self.get_queryset().order_by('-pk')
        context["other_scholarships"] = self.get_queryset().filter(otherscholarshipapplication__isnull=False)
        context['mastercard_scholarship'] = self.get_queryset().filter(mastercardscholarshipapplication__isnull=False)

        context["types"] = Call.SCHOLARSHIP_TYPES
        context["per_page"] = self.request.POST.get('per_page')
        # tag_ids = list(set(Scholarshipapplication.objects.values_list('tags', flat=True)))
        # context["tags"] = Tags.objects.filter(id__in=tag_ids)
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('first_name') or self.request.POST.get('last_name') or
                self.request.POST.get('call_id') or self.request.POST.get('programme')
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

    def export_to_excel(self, request, context):
        fd, file_name = tempfile.mkstemp()
        os.close(fd)
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '$#,##0'})

        headers = [
            'Id',
            'Name Of University',
            'Programme',
            'Call ID',
            'Last Name',
            'First Name',
            'Nationality',
            'Gender',
            'Age',
            'Business Address',
            'Business Email',

            'Mobile Telephone',
            'Village of birth',
            'District of birth',
            'Country of birth',
            'Village of residence',
            'District of residence',
            'Nearest major road',
            'Telephone contact',
            'Telephone owner',

            # 'Father'
            # 'MOther'
            'Name of guardian or spouse',
            'Guardian / spouse phone',
            'Guardian relationship',
            'Guardian or Spouses occupation',
            'Number of siblings',
            # publications and research is a list
            # Family associated information is a list
            # 'Who contributes most to income',
            'own livestock',
            'No. of Donkeys',
            'No. of camels',
            'No. of chicken',
            'No. of cattle',
            'No.of goats',
            'No. of sheep',
            'Electricity connection',
            'Toilet type',
            'Number of toilet users',
            'Major watersource',
            'Other water source',
            'Distance to water source(KM)',
            # 'Type of roofing',
            # housewall
            # floor
            # Assets
            'Income source 1',
            'Income source 2',
            'Income source 3',
            'Income source 4',
            'House rooms',
            'No. of people living in the house',
            'Had school balance',
            'School balances',
            # Leadership positions
            'Experience with agriculture',
            'Most Important problem faced in life',
            'Preferred sector 1',
            'Preferred sector 2',
            'Preferred sector 3',
            # work experience
            'Undergraduate degree program',
            'Grading criteria',
            # 'Grade',
            'Institution',
            'Year of completion',
            'Most significant contribution',
            'Have disability',
            'Specify disability',
            'History of chronic illness',
            'specify chronic illness',
            'Ever arrested',
            'Offense',
            'Used English as Language of instruction',
            'Scholarship call source',

        ]
        # Write some data headers.
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Start from the first cell below the headers.
        row = 1
        col = 0

        scholarships = context['mastercard_scholarship']
        # Iterate over the data and write it out row by row.
        for scholarship in scholarships:
            # get mastercard scholarship data
            try:
                master = scholarship.mastercardscholarshipapplication
            except:
                master = None
            # get parent information
            parent = Parent.objects.filter(application=scholarship.id)
            fields = [
                scholarship.pk,
                master.name_of_university if master else '',
                scholarship.programme_applied_for,
                scholarship.call.call_id if scholarship.call else '',
                scholarship.user.last_name,
                scholarship.user.first_name,
                master.get_country_of_residence_display() if master else '',
                scholarship.user.get_gender_display(),
                date.today().year - scholarship.date_of_birth.year if (master and scholarship.date_of_birth) else '',
                scholarship.user.business_address,
                scholarship.user.business_email,
                str(scholarship.user.mobile),
                master.village_of_birth if master else '',
                master.district_of_birth if master else '',
                master.get_country_of_birth_display() if master else '',
                master.village_of_residence if master else '',
                master.district_of_residence if master else '',
                master.nearest_major_road if master else '',

                str(master.telephone_contacts) if master else '',
                str(master.telephone_owner) if master else '',
                master.name_of_guardian_or_spouse if master else '',
                str(master.guardian_or_spouse_phone) if master else '',
                master.guardian_relationship if master else '',
                master.guardian_occupation if master else '',
                master.number_of_siblings if master else '',
                master.own_livestock if master else '',
                master.number_of_donkeys if master else '',
                master.number_of_camels if master else '',
                master.number_of_chickens if master else '',
                master.number_of_cattle if master else '',
                master.number_of_goats if master else '',
                master.number_of_sheep if master else '',
                master.electricity if master else '',
                master.toilet_type if master else '',
                master.how_many_share_toilet if master else '',
                master.water_source if master else '',
                master.other_water_source if master else '',
                master.distance_to_the_source if master else '',
                # master.type_of_roofing,
                master.income_source_1 if master else '',
                master.income_source_2 if master else '',
                master.income_source_3 if master else '',
                master.income_source_4 if master else '',
                master.rooms_in_house if master else '',
                master.people_in_house if master else '',
                master.pending_high_school_balances if master else '',
                master.school_balances if master else '',
                master.experience if master else '',
                master.challenge if master else '',
                master.sector_1 if master else '',
                master.sector_2 if master else '',
                master.sector_3 if master else '',
                # work experience
                master.degree_program if master else '',
                master.grading_creteria if master else '',
                # master.total_score, #this needs to be checked
                master.institution if master else '',
                master.year_of_completion if master else '',
                master.most_significant_contribution if master else '',
                master.have_physical_disability if master else '',
                master.physical_disability if master else '',
                master.have_history_of_chronic_illness if master else '',
                master.history_of_chronic_illness if master else '',
                master.have_been_arrested if master else '',
                master.cause_of_arrest if master else '',
                scholarship.english_in_high_school if master else '',
                scholarship.scholarship_call_source if master else '',

                # parent.all()[:1].get(),

            ]
            for col, field in enumerate(fields):
                worksheet.write(row, col, field)

            row += 1

        workbook.close()

        fh = open(file_name, 'rb')
        resp = fh.read()
        fh.close()
        response = HttpResponse(resp)
        response['Content-Type'] = 'application/ms-excel'
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % \
                                          ("applications",)
        return response

    def export_excel_report(self, request, context):
        fd, file_name = tempfile.mkstemp()
        os.close(fd)
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '$#,##0'})

        headers = [
            'Id',
            'Name Of University',
            'Programme',
            'Call ID',
            'Last Name',
            'First Name',
            'Nationality',
            'Gender',
            'Age',
            'Business Address',
            'Business Email',
            # 'Mobile Telephone',
        ]
        # Write some data headers.
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Start from the first cell below the headers.
        row = 1
        col = 0

        scholarships = self.get_queryset().filter(otherscholarshipapplication__isnull=False)
        # Iterate over the data and write it out row by row.
        for scholarship in scholarships:
            try:
                other = scholarship.otherscholarshipapplication
            except:
                other = None
            fields = [
                scholarship.pk,
                other.name_of_university if other else '',
                scholarship.programme_applied_for,
                scholarship.call.call_id if scholarship.call else '',
                scholarship.user.last_name,
                scholarship.user.first_name,
                other.get_country_of_residence_display() if other else '',
                scholarship.user.get_gender_display(),
                date.today().year - scholarship.date_of_birth.year if (other and scholarship.date_of_birth) else '',
                scholarship.user.business_address,
                scholarship.user.business_email,
                str(scholarship.user.mobile)
            ]
            for col, field in enumerate(fields):
                worksheet.write(row, col, field)

            row += 1

        workbook.close()

        fh = open(file_name, 'rb')
        resp = fh.read()
        fh.close()
        response = HttpResponse(resp)
        response['Content-Type'] = 'application/ms-excel'
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % \
                                          ("applications",)
        return response

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'export-excel' in request.POST:
            return self.export_to_excel(request, context)

        if 'export-report' in request.POST:
            return self.export_excel_report(request, context)

        return self.render_to_response(context)


class ScholarshipsReviewListView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "scholarships_list"
    template_name = "scholarship_reviews.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            submitted=True,
            selected_for_funding__isnull=True
        ).exclude(
            reviews__reviewer=self.request.user
        ).distinct()

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    call__call_id__icontains=request_post.get('call_id'))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    otherscholarshipapplication__programme_applied_for__contains=request_post.get('programme'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ScholarshipsReviewListView, self).get_context_data(**kwargs)
        context["scholarships"] = self.get_queryset().order_by('-pk')
        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None
        search = False
        if (
                self.request.POST.get('first_name') or self.request.POST.get('last_name') or
                self.request.POST.get('call_id') or self.request.POST.get('programme')
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


class ScholarshipReviewReportView(LoginRequiredMixin, DetailView):
    model = Call
    context_object_name = "scholarships_list"
    template_name = "scholarship_reviews.html"

    def get_context_data(self, **kwargs):
        report_data = []
        self.object = self.get_object()
        for application in Scholarshipapplication.objects.filter(call=self.object):
            reviews = Scholarshipappreview.objects.filter(
                application=application
            ).aggregate(Sum('mark'), Avg('mark'))
            data = {
                'application': application,
                'score': reviews['mark__sum'],
                'mean_score': reviews['mark__avg']
            }
            report_data.append(data)

        context = super(ScholarshipReviewReportView, self).get_context_data(**kwargs)

        context["report_data"] = report_data

        return context

    def export_to_excel(self, request, context):
        fd, file_name = tempfile.mkstemp()
        os.close(fd)
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '$#,##0'})

        headers = [
            'Id',
            'Full Name',
            'Nationality',
            'Gender',
            'Masters Thesis Title',
            'Review Marks',
            'Review Mean Mark',
            'Review Rank'
            'Review Comments',
        ]
        # Write some data headers.
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Start from the first cell below the headers.
        row = 1
        col = 0

        report_data = context['report_data']
        # Iterate over the data and write it out row by row.
        for data in report_data:
            scholarship = data['application']
            fields = [
                scholarship.pk,
                scholarship.user.get_full_name(),
                scholarship.user.nationality,
                scholarship.user.get_gender_display(),
                scholarship.otherscholarshipapplication.masters_thesis_title,
                data['score'],
                data['mean_score'],
                '',
                ''
            ]
            for col, field in enumerate(fields):
                worksheet.write(row, col, field)

            row += 1

        workbook.close()

        fh = open(file_name, 'rb')
        resp = fh.read()
        fh.close()
        response = HttpResponse(resp)
        response['Content-Type'] = 'application/ms-excel'
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % \
                                          ("ReviewerReport",)
        return response

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.export_to_excel(request, context)


class MastercardReviewListView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "scholarships_list"
    template_name = "scholarship_review_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            reviewers=self.request.user,
            # submitted=True,
            selected_for_funding__isnull=True, state='validated', reviews__isnull=True,
        ).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(state='validated').order_by('-id')

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    call__call_id__icontains=request_post.get('call_id'))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    otherscholarshipapplication__programme_applied_for__contains=request_post.get('programme'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(MastercardReviewListView, self).get_context_data(**kwargs)

        context["scholarships"] = self.get_queryset().order_by('-pk')

        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('first_name') or self.request.POST.get('last_name') or
                self.request.POST.get('call_id') or self.request.POST.get('programme')
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


class SelectCallView(LoginRequiredMixin, CreateView):
    model = Scholarshipapplication
    form_class = SelectCallForm
    template_name = "select_scholarship_call.html"

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
        if call.scholarship_type == 'mastercard':
            return redirect("scholarships:add_mastercard_application", call.pk)
        else:
            return redirect("scholarships:add_application", call.pk)

    def form_invalid(self, form, other_form):
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(SelectCallView, self).get_context_data(**kwargs)
        context['call'] = Call.objects.filter(
            scholarship_type__isnull=False, submission_deadline__gte=datetime.date.today())
        print("context", context, "kwargs", kwargs)
        return context


# create mastercard scholarship
class CreateMastercardScholarshipView(LoginRequiredMixin, CreateView):
    model = Scholarshipapplication
    form_class = ScholarshipForm
    template_name = "create_mastercard_scholarship_application.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateMastercardScholarshipView, self).dispatch(request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        initial = super(CreateMastercardScholarshipView, self).get_initial(**kwargs)
        initial['call'] = Call.objects.get(pk=self.kwargs['call_pk'])
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['gender'] = self.request.user.gender
        initial['country_of_residence'] = self.request.user.country
        initial['contact_email'] = self.request.user.business_email
        initial['country_of_residence'] = self.request.user.nationality
        initial['country_of_birth'] = self.request.user.country
        return initial

    def get_form_kwargs(self):
        kwargs = super(CreateMastercardScholarshipView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.mastercard_form = MastercardscholarshipapplicationForm(request.POST, request.FILES)
        self.education = MastercardeducationFormSet(request.POST, request.FILES, prefix='education_set')
        self.parent = ParentFormSet(request.POST, request.FILES, prefix='parent_set')
        self.income = HouseholdincomesourceFormSet(request.POST, request.FILES, prefix='incomesource_set')
        self.research = ResearchFormSet(request.POST, request.FILES, prefix='research_set')
        self.position = LeadershippositionFormSet(request.POST, request.FILES, prefix='position_set')
        self.experience = WorkexperienceFormSet(request.POST, request.FILES, prefix='experience_set')
        formsets_valid = (
                self.education.is_valid() and self.experience.is_valid() and self.parent.is_valid() and self.income.is_valid() and
                self.research.is_valid() and self.position.is_valid()
        )
        if form.is_valid() and self.mastercard_form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            print(self.mastercard_form.errors)
            print(self.education)
            print(self.parent)
            print(self.income)
            print(self.research)
            print(self.position)
            print(self.experience)
        return self.form_invalid(form, self.mastercard_form)

    def form_valid(self, form):
        try:
            # Save Scholarship application
            application = form.save(commit=False)
            application.user = self.request.user
            application.save()
            mastercard = self.mastercard_form.save(commit=False)
            mastercard.scholarshipapplication_ptr = application
            mastercard.save()
            self.education.instance = application
            self.education.save()
            self.parent.instance = application
            instances = self.parent.save(commit=False)
            relationships = ['father', 'mother']
            for i, parent in enumerate(instances):
                parent.relationship = relationships[i]
                parent.save()
            self.research.instance = application
            self.research.save()
            self.income.instance = application
            self.income.save()
            self.position.instance = application
            self.position.save()
            self.experience.instance = application
            self.experience.save()

            # sending email to the applicant after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Scholarship Application'
            message = render_to_string('scholarship_application_confirmation_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': application
            })
            email = EmailMessage(mail_subject, message, to=[self.request.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

            if self.request.POST.get("savenewform"):
                return redirect("scholarships:list")

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy('scholarships:list'), 'error': False}
                return JsonResponse(data)
            messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application Submitted successfully.')
            return redirect("scholarships:list")
        except IntegrityError:
            messages.add_message(self.request, messages.WARNING, 'You can not apply more than once for the same call.')
            return redirect("scholarships:list")

    def form_invalid(self, form, mastercard_form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form, mastercard_form=mastercard_form,
                                  education=self.education, parent=self.parent, income=self.income,
                                  position=self.position, research=self.research, experience=self.experience, )
        )

    def get_context_data(self, **kwargs):
        context = super(CreateMastercardScholarshipView, self).get_context_data(**kwargs)
        context["scholarship_form"] = context["form"]
        user = self.request.user

        print("kwargs", self.kwargs)
        # context['call'] = Call.objects.get(pk=self.kwargs['call_pk'])
        context["mastercard_form"] = context.get('mastercard_form') or MastercardscholarshipapplicationForm()
        context['parent_formset'] = context.get('parent') or ParentFormSet(prefix='parent_set')
        context['education_formset'] = context.get('education') or MastercardeducationFormSet(prefix='education_set')
        context['incomesource_formset'] = context.get('income') or HouseholdincomesourceFormSet(
            prefix='incomesource_set')
        context['research_formset'] = context.get('research') or ResearchFormSet(prefix='research_set')
        context['position_formset'] = context.get('position') or LeadershippositionFormSet(prefix='position_set')
        context['experience_formset'] = context.get('experience') or WorkexperienceFormSet(prefix='experience_set')
        context['school_types'] = [
            'Primary Education',
            'Ordinary level; UCE for Uganda, KCSE for Kenya and/or equivalent from other countries',
            'Advanced level/High School Certificate for Uganda and/or equivalent from other countries',
            'Tertiary level certificate/Diploma',
            'University Education (only filled by those applying for Masters degrees)',
        ]
        context['parents'] = ['Father', 'Mother']
        return context


class CreateScholarshipView(LoginRequiredMixin, CreateView):
    model = Scholarshipapplication
    form_class = ScholarshipForm
    template_name = "create_scholarship_application.html"

    def dispatch(self, request, *args, **kwargs):

        # self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateScholarshipView, self).dispatch(request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        initial = super(CreateScholarshipView, self).get_initial(**kwargs)
        initial['call'] = Call.objects.get(pk=self.kwargs['call_pk'])
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['gender'] = self.request.user.gender
        initial['country_of_residence'] = self.request.user.country
        initial['contact_email'] = self.request.user.business_email
        return initial

    def get_form_kwargs(self):
        kwargs = super(CreateScholarshipView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.other_form = OtherForm(request.POST, request.FILES)
        self.education = EducationFormSet(request.POST, request.FILES, prefix='education_set')
        self.research = ResearchFormSet(request.POST, request.FILES, prefix='research_set')
        self.publications = PublicationsFormSet(request.POST, request.FILES, prefix='publication_set')
        self.employment = EmploymenthistoryFormSet(request.POST, request.FILES, prefix='employment_set')
        self.referees = ReferenceletterFormSet(request.POST, request.FILES, prefix='referee_set')
        # self.transcripts = TranscriptfileFormSet(request.POST, request.FILES, prefix='transcript_set')
        formsets_valid = (
                self.education.is_valid() and self.employment.is_valid() and self.referees.is_valid() and
                self.research.is_valid() and self.publications.is_valid()
        )
        if form.is_valid() and self.other_form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            print(self.other_form.errors)
            print(self.education.errors)
            print(self.research.errors)
            print(self.publications.errors)
            print(self.employment.errors)
            print(self.referees.errors)

        return self.form_invalid(form, self.other_form)

    def form_valid(self, form):
        try:
            # Save Scholarshipapplication
            application = form.save(commit=False)

            application.user = self.request.user

            application.save()
            other = self.other_form.save(commit=False)
            other.scholarshipapplication_ptr = application
            other.save()

            self.education.instance = application
            self.education.save()
            self.research.instance = application
            self.research.save()
            self.publications.instance = application
            self.publications.save()
            self.employment.instance = application
            self.employment.save()
            self.referees.instance = application
            self.referees.save()
            # self.transcripts.instance = application
            # self.transcripts.save()

            # sending email to the applicant after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Scholarship Application'
            message = render_to_string('scholarship_application_confirmation_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': application
            })
            email = EmailMessage(mail_subject, message, to=[self.request.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

            if self.request.POST.get("savenewform"):
                return redirect("scholarships:list")

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy('scholarships:list'), 'error': False}
                return JsonResponse(data)
            messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application Submitted successfully.')
            return redirect("scholarships:list")

        except IntegrityError:
            messages.add_message(self.request, messages.WARNING, 'You can not apply more than once for the same call.')
            return redirect("scholarships:list")

    def form_invalid(self, form, other_form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form, other_form=other_form,
                                  education=self.education, employment=self.employment, referees=self.referees,
                                  research=self.research, publications=self.publications, )
        )

    def get_context_data(self, **kwargs):
        context = super(CreateScholarshipView, self).get_context_data(**kwargs)
        context["scholarship_form"] = context["form"]
        user = self.request.user
        initial = {
            'title': user.title,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'country': user.country,
            'nationality': user.nationality,
        }
        context["profile_form"] = MastercardscholarshipapplicationForm(initial=initial)
        context["other_form"] = context.get('other_form') or OtherForm()
        context['education_formset'] = context.get('education') or EducationFormSet(prefix='education_set')
        context['research_formset'] = context.get('research') or ResearchFormSet(prefix='research_set')
        context['publications_formset'] = context.get('publications') or PublicationsFormSet(prefix='publication_set')
        context['employment_formset'] = context.get('employment') or EmploymenthistoryFormSet(prefix='employment_set')
        context['referee_formset'] = context.get('referees') or ReferenceletterFormSet(prefix='referee_set')
        # context['transcript_formset'] = context.get('transcripts') or TranscriptfileFormSet(prefix='transcript_set')
        return context


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Scholarshipappreview
    form_class = ScholarshipappreviewForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.application = get_object_or_404(
            Scholarshipapplication, id=request.POST.get('application'))
        if (
                request.user.is_superuser or
                request.user.has_perm('scholarships.mark_scholarship_applications')
        ):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)

        data = {
            'error': "You don't have permission to review for this account."}
        return JsonResponse(data)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.application = self.application
        review.reviewer = self.request.user
        review.save()
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application Review Submitted successfully.')
        return redirect('common:home')

    def form_invalid(self, form):
        context = {}
        print(form.errors)
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return render(self.request, 'view_scholarship.html', context)
        # return JsonResponse({"error": form.errors})


class ScholarshipapplicationReviewView(LoginRequiredMixin, DetailView):
    model = Scholarshipapplication
    context_object_name = "applicationrecord"
    template_name = "review_scholarship.html"

    def get_template_names(self):
        application = self.get_object()
        if application.call.scholarship_type == "mastercard":
            template_name = 'review_mastercard_scholarship.html'
        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(ScholarshipapplicationReviewView, self).get_context_data(**kwargs)
        applicationrecord = context["applicationrecord"]

        review_permission = True if (
                self.request.user == applicationrecord.user or
                self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        context.update({
            "reviews": applicationrecord.reviews.all(),
            "researchandpublications": applicationrecord.researchandpublications.all(),
            "application_record": applicationrecord,
            "review_form": ScholarshipappreviewForm()

        })
        return context


class ScholarshipapplicationDetailView(LoginRequiredMixin, DetailView):
    model = Scholarshipapplication
    context_object_name = "applicationrecord"
    template_name = "view_scholarship.html"

    def get_template_names(self):
        application = self.get_object()
        if application.call.scholarship_type == "mastercard":
            template_name = 'view_mastercard_scholarship.html'
        elif application.call.scholarship_type is None:
            return [template_name]

        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(ScholarshipapplicationDetailView, self).get_context_data(**kwargs)
        applicationrecord = context["applicationrecord"]

        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #    if self.request.user != applicationrecord.created_by:
        #        raise PermissionDenied

        review_permission = True if (
                self.request.user == applicationrecord.user or
                self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        context.update({
            "reviews": applicationrecord.reviews.all(),
            "application_record": applicationrecord,
            "publications": ResearchAndPublication.objects.filter(application=applicationrecord.id).order_by('code'),
            "referees": Referenceletter.objects.filter(application=applicationrecord.id),
            "publication_papers": Publication.objects.filter(application=applicationrecord.id),
            "review_form": ScholarshipappreviewForm(),
            "family_backgrounds": Parent.objects.filter(application=applicationrecord.id),
            "Household_incomesource": Householdincomesource.objects.filter(application=applicationrecord.id),
            # "Typeofroofingmaterial": Typeofroofingmaterial.objects.filter(application=applicationrecord.id),
            # "Leadership_positions": Leadershipposition.objects.filter(application=applicationrecord.id),
            #      "Incomecontributor": Incomecontributor.objects.filter(application=applicationrecord.id),
            # "work_experiences":Workexperience.objects.filter(application=applicationrecord.id),
            'parents': ['Father', 'Mother']

        })
        return context


class UpdateMastercardScholarshipView(LoginRequiredMixin, UpdateView):
    model = Scholarshipapplication
    form_class = ScholarshipForm
    template_name = "create_mastercard_scholarship_application.html"

    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMastercardScholarshipView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateMastercardScholarshipView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.mastercard_form = MastercardscholarshipapplicationForm(request.POST, request.FILES)
        self.education = EducationFormSet(request.POST, request.FILES, prefix='education_set')
        self.parent = ParentFormSet(request.POST, request.FILES, prefix='parent_set')
        self.income = HouseholdincomesourceFormSet(request.POST, request.FILES, prefix='incomesource_set')
        self.research = ResearchFormSet(request.POST, request.FILES, prefix='research_set')
        self.position = LeadershippositionFormSet(request.POST, request.FILES, prefix='position_set')
        self.experience = WorkexperienceFormSet(request.POST, request.FILES, prefix='experience_set')
        formsets_valid = (
                self.education.is_valid() and self.experience.is_valid() and self.parent.is_valid() and self.income.is_valid() and
                self.research.is_valid() and self.position.is_valid()
        )
        if form.is_valid() and self.mastercard_form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            print(self.mastercard_form.errors)
        return self.form_invalid(form, self.mastercard_form)

    def form_valid(self, form):
        # Save Scholarship application
        application = form.save(commit=False)
        if 'savefinal' in self.request.POST:
            print("will save final")
            application.submitted = True
        else:
            print("save draft")
        application.save()
        application.user = self.request.user
        application.save()
        self.parent.instance = application
        self.parent.save(commit=False)
        instances = application.parent_set.all().order_by('pk')
        print("instances", instances)
        relationships = ['father', 'mother']
        for i, parent in enumerate(instances):
            parent.relationship = 'rel-{}'.format(i)
            parent.save()
        for i, parent in enumerate(instances):
            print("relationship", relationships[i])
            parent.relationship = relationships[i]
            parent.save()

        self.education.instance = application
        instances = self.education.save()
        school_types = [
            'primary',
            'olevel',
            'alevel',
            'tertiary',
            'university',
        ]
        for i, edu in enumerate(instances):
            edu.particular = school_types[i]
            edu.save()

        self.income.instance = application
        self.income.save()
        self.research.instance = application
        self.research.save()
        self.position.instance = application
        self.position.save()
        self.experience.instance = application
        self.experience.save()

        if self.request.POST.get("savenewform"):
            return redirect("scholarships:list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'scholarships:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application updated successfully.')
        return redirect("scholarships:list")

    def form_invalid(self, form, mastercard_form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form, parent=self.parent,
                                  education=self.education, income=self.income, position=self.position,
                                  research=self.research,
                                  experience=self.experience)
        )

    def get_context_data(self, **kwargs):
        context = super(UpdateMastercardScholarshipView, self).get_context_data(**kwargs)
        context["scholarship_obj"] = self.object
        context["scholarship_form"] = context["form"]
        user = self.request.user
        print("kwargs", self.kwargs)
        # context['call'] = Call.objects.get(pk=self.kwargs['call'])
        context["mastercard_form"] = context.get('mastercard_form') or MastercardscholarshipapplicationForm()
        context['parent_formset'] = context.get('parent') or ParentFormSet(prefix='parent_set')
        context['education_formset'] = context.get('education') or MastercardeducationFormSet(prefix='education_set')
        context['incomesource_formset'] = context.get('income') or HouseholdincomesourceFormSet(
            prefix='incomesource_set')
        context['research_formset'] = context.get('research') or ResearchFormSet(prefix='research_set')
        context['position_formset'] = context.get('position') or LeadershippositionFormSet(prefix='position_set')
        context['experience_formset'] = context.get('experience') or WorkexperienceFormSet(prefix='experience_set')
        context['school_types'] = [
            'Primary Education',
            'Ordinary level; UCE for Uganda, KCSE for Kenya and/or equivalent from other countries',
            'Advanced level/High School Certificate for Uganda and/or equivalent from other countries',
            'Tertiary level certificate/Diploma',
            'University Education (only filled by those applying for Masters degrees)',
        ]
        context['parents'] = ['Father', 'Mother']
        return context


class UpdateScholarshipView(LoginRequiredMixin, UpdateView):
    model = Scholarshipapplication
    form_class = ScholarshipForm
    template_name = "create_scholarship_application.html"

    def dispatch(self, request, *args, **kwargs):

        return super(UpdateScholarshipView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateScholarshipView, self).get_form_kwargs()

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.other_form = OtherForm(request.POST, request.FILES, instance=self.object.otherscholarshipapplication)
        self.education = EducationFormSet(request.POST, request.FILES, prefix='education_set', instance=self.object)
        self.research = ResearchFormSet(request.POST, request.FILES, prefix='research_set', instance=self.object)
        self.employment = EmploymenthistoryFormSet(request.POST, request.FILES, prefix='employment_set',
                                                   instance=self.object)
        self.referees = ReferenceletterFormSet(request.POST, request.FILES, prefix='referee_set', instance=self.object)
        # self.transcripts = TranscriptfileFormSet(request.POST, request.FILES, prefix='transcript_set', instance=self.object)
        formsets_valid = (
                self.education.is_valid() and self.employment.is_valid() and self.referees.is_valid()
        )
        if form.is_valid() and self.other_form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            print(self.other_form.errors)
            print("formsets valid", formsets_valid)
            print("educ", self.education.errors)
            print("Research", self.research.errors)
            print("employment", self.employment.errors)
            print("referees", self.referees.errors)
        return self.form_invalid(form, self.other_form)

    def form_valid(self, form):
        # Save Scholarshipapplication
        application = form.save(commit=False)
        if 'savefinal' in self.request.POST:
            print("will save final")
            application.submitted = True
        else:
            print("save draft")
        application.save()
        other = self.other_form.save(commit=False)
        other.scholarshipapplication_ptr = application
        other.save()
        self.education.instance = application
        self.education.save()
        self.employment.instance = application
        self.employment.save()
        self.research.instance = application
        self.research.save()
        self.referees.instance = application
        self.referees.save()

        if self.request.POST.get("savenewform"):
            return redirect("scholarships:list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'scholarships:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application Updated successfully.')
        return redirect("scholarships:list")

    def form_invalid(self, form, other_form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form, other_form=other_form,
                                  education=self.education, employment=self.employment, referees=self.referees,
                                  research=self.research,
                                  )
        )

    def get_context_data(self, **kwargs):
        context = super(UpdateScholarshipView, self).get_context_data(**kwargs)
        context["scholarship_obj"] = self.object
        '''
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != context['callobj'].created_by:
                raise PermissionDenied
        '''
        context["scholarship_form"] = context["form"]
        try:
            context["other_form"] = context.get('other_form') or OtherForm(
                instance=self.object.otherscholarshipapplication)
        except:
            context["other_form"] = OtherForm()
        context['education_formset'] = context.get('education') or EducationFormSet(instance=self.object,
                                                                                    prefix='education_set')
        context['research_formset'] = context.get('research') or ResearchFormSet(instance=self.object,
                                                                                 prefix='research_set')
        context['employment_formset'] = context.get('employment') or EmploymenthistoryFormSet(instance=self.object,
                                                                                              prefix='employment_set')
        context['referee_formset'] = context.get('referees') or ReferenceletterFormSet(instance=self.object,
                                                                                       prefix='referee_set')
        return context


class ScholarshipapplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Scholarshipapplication
    template_name = 'scholarships.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("scholarships:list")


# reviewed scholarships
class ReviewedScholorshipListView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "scholarships_list"
    template_name = "scholarship_reviewed_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            reviewers=self.request.user.pk,
            reviews__isnull=False
            # selected_for_funding__isnull=True
        ).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(
                name='Grants Managers').exists() or self.request.user.groups.filter(
            name='Scholarship Managers').exists():
            queryset = self.model.objects.filter(reviews__isnull=False).order_by('-id')

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    call__call_id__icontains=request_post.get('call_id'))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    otherscholarshipapplication__programme_applied_for__contains=request_post.get('programme'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ReviewedScholorshipListView, self).get_context_data(**kwargs)
        context["scholarships"] = self.get_queryset().order_by('-pk')
        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('first_name') or self.request.POST.get('last_name') or
                self.request.POST.get('call_id') or self.request.POST.get('programme')
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


# assigning scholarship applications to reviewers
class CreatScholarReviewerView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    form_class = ScholarshipReviewerForm
    template_name = "assign_scholarship_reviewers.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            state='submitted'
        ).distinct().order_by('-id')

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('applicant_name')) |
                    Q(user__last_name__icontains=request_post.get('applicant_name')))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    Q(programme_applied_for__icontains=request_post.get('programme')))

            if request_post.get('call_id'):
                queryset = queryset.filter(
                    Q(call__call_id__icontains=request_post.get('call_id')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["scholarship_applications"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context["reviewerform"] = ScholarshipReviewerForm
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


class ScholarshipapplicationRewiewDetailView(LoginRequiredMixin, DetailView):
    model = Scholarshipapplication
    context_object_name = "applicationrecord"
    template_name = "view_scholarship_Review.html"

    def get_template_names(self):
        application = self.get_object()
        if application.call.scholarship_type == "mastercard":
            template_name = 'view_scholarship_Review_mastercard.html'
        elif application.call.scholarship_type is None:
            return [template_name]

        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(ScholarshipapplicationRewiewDetailView, self).get_context_data(**kwargs)
        applicationrecord = context["applicationrecord"]

        review_permission = True if (
                self.request.user == applicationrecord.user or
                self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        context.update({
            "reviews": applicationrecord.reviews.all(),
            "application_record": applicationrecord,
            "publications": ResearchAndPublication.objects.filter(application=applicationrecord.id).order_by('code'),
            "review_form": ScholarshipappreviewForm(),
            "average_score": applicationrecord.reviews.all().aggregate(Avg('mark')),
            "reject_form": ScholarshipApplicationRejectForm()

        })
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(ScholarshipapplicationRewiewDetailView, self).get_initial(**kwargs)
        initial.update({
            'selected_for_funding_comments': 'After double reviewing your application by external reviewers, we regret to inform you that your application did not go through. We however, encourage you to apply for subsequent calls.',

        })
        return initial


# assign scholarship reviewer post method
class AssignReviewerView(LoginRequiredMixin, TemplateView):
    template_name = "assign_scholarship_reviewers.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssignReviewerView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssignReviewerView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = ScholarshipReviewerForm(request.POST, request=request)
        if form.is_valid():
            scholarship_application_ids = request.POST.getlist('application')
            list_of_obj = Scholarshipapplication.objects.filter(pk__in=scholarship_application_ids)
            list_of_reviewers = request.POST.getlist('reviewers')
            for application in list_of_obj:
                form.save(commit=False)
                application.scholarship_manager = self.request.user
                application.reviewers.set(list_of_reviewers)
                application.save()
            for user in application.reviewers.all():
                current_site = get_current_site(self.request)
                subject = 'SCHOLARSHIP APPLICATION REVIEW REQUEST'
                message = render_to_string('scholarship_application_review_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'applications': list_of_obj
                })
            user.email_user(subject, message)
            # sending email to the  grants manager after submission

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                    'scholarships:list'), 'error': False}
                return redirect("scholarships:list")
            messages.add_message(self.request, messages.SUCCESS,
                                 'Scholarship Application Reviewers assigned  successfully.')
            return redirect("scholarships:list")


# print  call details
class ScholarshipPrintView(LoginRequiredMixin, DetailView, WeasyTemplateResponseMixin):
    model = Scholarshipapplication
    context_object_name = "applicationrecord"
    template_name = "print_scholarship.html"
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # suggested filename (is required for attachment!)
    pdf_filename = 'scholarship_details.pdf'

    def get_template_names(self):
        application = self.get_object()
        if application.call.scholarship_type == "mastercard":
            template_name = 'print_scholarship_Review_mastercard.html'
        elif application.call.scholarship_type is None:
            return [template_name]

        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(ScholarshipPrintView, self).get_context_data(**kwargs)
        applicationrecord = context["applicationrecord"]

        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #    if self.request.user != applicationrecord.created_by:
        #        raise PermissionDenied

        review_permission = True if (
                self.request.user == applicationrecord.user or
                self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        context.update({
            "reviews": applicationrecord.reviews.all(),
            "application_record": applicationrecord,
            "publications": ResearchAndPublication.objects.filter(application=applicationrecord.id).order_by('code'),
            "referees": Referenceletter.objects.filter(application=applicationrecord.id),
            "publication_papers": Publication.objects.filter(application=applicationrecord.id),
            "review_form": ScholarshipappreviewForm(),
            "family_backgrounds": Parent.objects.filter(application=applicationrecord.id),
            "Household_incomesource": Householdincomesource.objects.filter(application=applicationrecord.id),
            # "Typeofroofingmaterial": Typeofroofingmaterial.objects.filter(application=applicationrecord.id),
            # "Leadership_positions": Leadershipposition.objects.filter(application=applicationrecord.id),
            #      "Incomecontributor": Incomecontributor.objects.filter(application=applicationrecord.id),
            # "work_experiences":Workexperience.objects.filter(application=applicationrecord.id),
            'parents': ['Father', 'Mother']

        })
        return context


class CreateScholarshipApprovalView(LoginRequiredMixin, CreateView):
    model = Scholarship
    form_class = ScholarshipApprovalForm
    template_name = "create_scholarship_approval.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateScholarshipApprovalView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateScholarshipApprovalView, self).get_form_kwargs()
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
        # Save Grant
        scholarship_object = form.save(commit=False)
        application = Scholarshipapplication.objects.get(pk=self.kwargs['pk'])
        scholarship_object.application = application
        scholarship_object.student = application.user
        scholarship_object.approved_by = self.request.user
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        reporting_period = form.cleaned_data['reporting_period']
        actual_start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
        actual_end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')
        delta = relativedelta.relativedelta(actual_end_date, actual_start_date)
        no_of_reports = int((delta.years * 12 + delta.months) / reporting_period)
        scholarship_object.report_number = no_of_reports
        scholarship_object.approval_status = 'approved'
        current_year = str(date.today().year)
        last_scholarship = Scholarship.objects.latest('id')
        generated_scholarship_number = 0
        # getting last call year
        last_scholarship_year = last_scholarship.scholarship_year
        last_inserted_generated_number = last_scholarship.generated_number
        if (last_scholarship_year == str(date.today().year)):
            generated_scholarship_number = last_inserted_generated_number + 1
        else:
            generated_scholarship_number = 0 + 1
        scholarship_object.scholarship_id = 'RU/' + str(application.call.scholarship_type) + "/" + current_year + '/' + \
                                            'S/' + str(format(int(generated_scholarship_number), "04"))
        # change applicant to student
        studentgroup = Group.objects.get(name='Students')
        application.user.groups.clear()
        application.user.groups.add(studentgroup)
        application.selected_for_funding = True
        application.state = 'selected_for_funding'
        application.selected_for_funding_comments = form.cleaned_data['selected_for_funding_comments']
        application.save()
        scholarship_object.save()
        form.save_m2m()
        # sending email to the selected student

        current_site = get_current_site(self.request)
        mail_subject = 'RUFORUM SCHOLARSHIP APPLICATION'
        message = render_to_string('scholarship_award_email.html', {
            'user': application.user,
            'domain': current_site.domain,
            'application': application

        })
        email = EmailMessage(mail_subject, message, to=[application.user.business_email],
                             from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        email.send()
        if self.request.POST.get("savenewform"):
            return redirect("grants:new_account")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'scholarships:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship approved successfully.')
        return redirect("scholarships:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateScholarshipApprovalView, self).get_context_data(**kwargs)
        context["scholarship_form"] = context["form"]
        application = Scholarshipapplication.objects.get(pk=self.kwargs['pk'])
        context['applicant'] = application.user
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(CreateScholarshipApprovalView, self).get_initial(**kwargs)
        application = Scholarshipapplication.objects.get(pk=self.kwargs['pk'])
        # catch exception for those
        try:
            if application.call.scholarship_type == 'mastercard':
                university = application.mastercardscholarshipapplication.name_of_university
            else:
                university = application.otherscholarshipapplication.name_of_university
        except:
            university = None
        initial.update({
            'institution': university,
            'programme_applied_for': application.programme_applied_for,
            'start_date': application.call.start_date,
            'end_date': application.call.end_date,

        })
        return initial


class ScholarshipApplicationRejectView(LoginRequiredMixin, UpdateView):
    model = Scholarshipapplication
    form_class = ScholarshipApplicationRejectForm
    template_name = "validate_application.html"

    def dispatch(self, request, *args, **kwargs):

        return super(ScholarshipApplicationRejectView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ScholarshipApplicationRejectView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("erors", form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save scholarship application
        applicationobject = form.save(commit=False)
        applicationobject.selected_for_funding = False
        applicationobject.state = 'rejected'
        applicationobject.save()
        # sending email to the rejected applicant

        current_site = get_current_site(self.request)
        mail_subject = 'RUFORUM SCHOLARSHIP APPLICATION'
        message = render_to_string('scholarship_reject_email.html', {
            'user': applicationobject.user,
            'domain': current_site.domain,
            'application': applicationobject

        })
        email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],
                             from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        email.send()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'scholarships:list'), 'error': False}
            return JsonResponse({'success_message': "Application Rejected"})
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application Rejected.')
        redirect("scholarships:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ScholarshipApplicationRejectView, self).get_context_data(**kwargs)
        context["applicationobj"] = self.object
        application_record = context["applicationobj"]

        context["applicationform"] = context["form"]
        return context


# scholarship application decisions
class ScholarshipsApplicationDecisionListView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "scholarships_list"
    template_name = "applications_decision.html"

    def get_queryset(self):
        state = ['rejected', 'selected_for_funding']
        queryset = self.model.objects.filter(state__in=state).order_by('-pk')
        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    call__call_id__icontains=request_post.get('call_id'))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    programme_applied_for__contains=request_post.get('programme'))
            if request_post.get('type'):
                queryset = queryset.filter(
                    call__scholarship_type__contains=request_post.get('type'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ScholarshipsApplicationDecisionListView, self).get_context_data(**kwargs)
        context["scholarships"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context["types"] = Call.SCHOLARSHIP_TYPES
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('first_name') or self.request.POST.get('last_name') or
                self.request.POST.get('call_id') or self.request.POST.get('programme')
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




# assign scholarship validators
class ScholarshipValidatorsView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "applications_list"
    form_class = ScholarshipValidatorForm
    template_name = "assign_scholarship_validators.html"

    def get_queryset(self):
        state = ['submitted']
        queryset = self.model.objects.filter(
            state__in=state
        ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists() \
                or self.request.user.groups.filter(name='Scholarship Managers').exists():
            queryset = self.model.objects.filter(state='submitted').order_by('-id')

        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(first_name__icontains=request_post.get('applicant_name')) |
                    Q(last_name__icontains=request_post.get('applicant_name')))
            if request_post.get('proposal_title'):
                queryset = queryset.filter(
                    Q(programme_applied_for__icontains=request_post.get('programme_applied_for')))

            if request_post.get('call_id'):
                queryset = queryset.filter(
                    Q(call__call_id__icontains=request_post.get('call_id')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["scholarship_applications"] = self.get_queryset()

        context["per_page"] = self.request.POST.get('per_page')

        context["applicationform"] = ScholarshipValidatorForm

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


# assign scholarship validators post method
class AssignScholarshipValidatorsView(LoginRequiredMixin, TemplateView):
    template_name = "assign_scholarship_validators.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssignScholarshipValidatorsView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssignScholarshipValidatorsView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = ScholarshipValidatorForm(request.POST, request=request)
        if form.is_valid():
            scholarship_application_ids = request.POST.getlist('application')
            list_of_obj = Scholarshipapplication.objects.filter(pk__in=scholarship_application_ids)
            list_of_validators = request.POST.getlist('validators')
            users_who_are_validators = User.objects.filter(pk__in=list_of_validators)
            print(list_of_obj)
            for application in list_of_obj:
                form.save(commit=False)
                application.scholarship_manager = self.request.user
                application.save()
                for validator in list_of_validators:
                    try:
                        application.validators.add(validator)
                    except IntegrityError:
                        try:
                            application.validators.add(validator)
                        except IntegrityError:
                            continue
                application.reviewers.set(list_of_validators)

            for user in users_who_are_validators:
                current_site = get_current_site(self.request)
                subject = 'SCHOLARSHIP APPLICATION VALIDATION REQUEST'
                message = render_to_string('scholarship_application_validation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'applications': list_of_obj
                })
                # user.email_user(subject, message)

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                    'scholarships:list'), 'error': False}
                return redirect("scholarships:list")
            messages.add_message(self.request, messages.SUCCESS,
                                 'Scholarship Application Reviewers assigned  successfully.')
            return redirect("scholarships:list")


class ScholarshipValidationListView(LoginRequiredMixin, TemplateView):
    model = Scholarshipapplication
    context_object_name = "scholarships_list"
    template_name = "scholarship_validation_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            validators=self.request.user,
            # submitted=True,
            selected_for_funding__isnull=True, state='submitted', reviews__isnull=True,
        ).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(
                name='Grants Managers').exists() or self.request.user.groups.filter(
                name='Scholarship Managers').exists():
            queryset = self.model.objects.filter(state='submitted', reviews__isnull=True).order_by('-id')

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    call__call_id__icontains=request_post.get('call_id'))
            if request_post.get('programme'):
                queryset = queryset.filter(
                    otherscholarshipapplication__programme_applied_for__contains=request_post.get('programme'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ScholarshipValidationListView, self).get_context_data(**kwargs)

        context["scholarships"] = self.get_queryset().order_by('-pk')

        context["per_page"] = self.request.POST.get('per_page')
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
                self.request.POST.get('first_name') or self.request.POST.get('last_name') or
                self.request.POST.get('call_id') or self.request.POST.get('programme')
        ):
            search = True

        context["search"] = search

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ScholarshipapplicationValidationView(LoginRequiredMixin, DetailView):
    model = Scholarshipapplication
    context_object_name = "applicationrecord"
    template_name = "validate_scholarship.html"

    def get_template_names(self):
        application = self.get_object()
        if application.call.scholarship_type == "mastercard":
            template_name = 'validate_mastercard_scholarship.html'
        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(ScholarshipapplicationValidationView, self).get_context_data(**kwargs)
        applicationrecord = context["applicationrecord"]

        review_permission = True if (
                self.request.user == applicationrecord.user or
                self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        context.update({
            "validations": applicationrecord.reviews.all(),
            "researchandpublications": applicationrecord.researchandpublications.all(),
            "application_record": applicationrecord,
            "validation_form": ScholarshipapplicationValidationForm()

        })
        return context


class ScholarshipApplicationValidateView(LoginRequiredMixin, UpdateView):
    model = Scholarshipapplication
    form_class = ScholarshipapplicationValidationForm
    template_name = "validate_scholarship.html"


    def dispatch(self, request, *args, **kwargs):
        return super(ScholarshipApplicationValidateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ScholarshipApplicationValidateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("erors", form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Grantapplication
        applicationobject = form.save(commit=False)
        compliant = form.cleaned_data['compliant']
        print("compliant", compliant)
        if compliant == 'c':
            applicationobject.state = 'validated'
        else:
            applicationobject.state = 'noncompliant'
        applicationobject.save()
        if applicationobject.state == 'validated':
            # send successful message to the applicant
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Scholarship Application Compliance '
            message = render_to_string('scholarship_application_compliance_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': applicationobject
            })
            email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()
        if applicationobject.state == 'noncompliant':
            # send successful message to the applicant
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Scholarship Application Compliance'
            message = render_to_string('scholarship_application_non_compliant_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': applicationobject,

            })
            email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Application Validated  successfully.')
        return redirect("scholarships:validation_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ScholarshipApplicationValidateView, self).get_context_data(**kwargs)
        context["application_record"] = self.object
        context["applicationform"] = context["form"]
        return context


# Edit leave application
class EditScholarshipView(LoginRequiredMixin, UpdateView):
    model = Scholarship
    form_class = EditScholarshipForm
    template_name = "edit_sholarship.html"

    def dispatch(self, request, *args, **kwargs):
        return super(EditScholarshipView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditScholarshipView, self).get_form_kwargs()
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
        # Save scholarship
        scholarship = form.save(commit=False)
        scholarship.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'scholarships:scholarship_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Updated successfully.')
        return redirect("scholarships:scholarship_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(EditScholarshipView, self).get_context_data(**kwargs)

        return context


# awarded scholarships
class AwardedScholarshipsListView(LoginRequiredMixin, TemplateView):
    model = Scholarship
    context_object_name = "scholarships_list"
    template_name = "awarded_scholarships.html"

    def get_queryset(self):
        queryset = self.model.objects.order_by('-id')


        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(AwardedScholarshipsListView, self).get_context_data(**kwargs)
        context["scholarships"] = self.get_queryset()
      
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ScholarshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for granted scholarships.
    """
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields =['application__call__call_id','scholarship_id','student__last_name','student__first_name','programme_applied_for','institution','start_date','end_date','reporting_period','report_number','approval_status','approved_by']

    def get_queryset(self):
     
        user = self.request.user
        queries= Scholarship.objects.order_by('-id')

        if self.request.user.is_superuser or self.request.user.groups.filter(name='Scholarship Managers').exists() or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = queries
        else:
        
            queryset = queries.filter(student=user)

        return queryset

# scholarship details
class AwardedScholarshipDetailView(LoginRequiredMixin, DetailView):
    model = Scholarship
    context_object_name = "scholarship"
    template_name = "view_awarded_scholarship.html"

    def get_context_data(self, **kwargs):
        context = super(AwardedScholarshipDetailView, self).get_context_data(**kwargs)
        scholarship = context["scholarship"]
        return context
