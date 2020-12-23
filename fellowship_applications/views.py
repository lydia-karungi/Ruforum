import datetime
import tempfile
import os
import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from .models import Fellowshipapplication, Fellowshipappreview
from contacts.models import User
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Avg
from django.db import transaction
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from calls.models import FellowshipCall
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import EmailMessage
#from applications.tasks import send_email
#from common.tasks import send_email_user_mentions
from .serializers import (FellowshipApplicationSerializer,FellowshipApplicationReviewSerializer,
FellowshipApplicationReviewSerializer)

from django.contrib.sites.shortcuts import get_current_site

from .forms import (
    FellowshipProfileForm, FellowshipapplicationForm,
     FellowshipappreviewForm,SelectCallForm,
    FellowshipapplicationValidateForm,
    FellowshipapplicationReviewersForm,FellowshipCarpappreviewForm, FellowshipapplicationValidatorsForm
)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

#Display list of fellowship applications
class FellowshipapplicationsListView(LoginRequiredMixin, TemplateView):
    model = Fellowshipapplication
    context_object_name = "applications_list"
    template_name = "fellowship_applications.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(status='submitted')
        if  not self.request.user.has_perm('fellowship_applications.change_fellowshipapplication') and  not self.request.user.is_superuser and not self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(user=self.request.user.id)
            print(queryset)
        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)

        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in = self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(first_name__icontains=request_post.get('applicant_name'))|
                    Q(last_name__icontains=request_post.get('applicant_name')))
            if request_post.get('state'):
                queryset = queryset.filter(
                    Q(state=request_post.get('state')))
            if request_post.get('home_institute'):
                queryset = queryset.filter(
                     Q(home_institute_name__icontains=request_post.get('home_institute')))
            if request_post.get('host_institute'):
                queryset = queryset.filter(
                   Q(host_institute_name__icontains=request_post.get('host_institute')))
            if request_post.get('call_id'):
                queryset = queryset.filter(
                   Q(call__call_id__icontains=request_post.get('call_id')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationsListView, self).get_context_data(**kwargs)
        context["fellowship_applications"] = self.get_queryset()
        context["states"] = Fellowshipapplication.APPLICATION_STATES
       
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
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def export_excel_report(self, request, context):
        fd, file_name = tempfile.mkstemp()
        os.close(fd)
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
         # Create a format for the date or time.
        date_format = workbook.add_format({'num_format':  'd mmm yyyy'})
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '$#,##0'})

        headers = [
        
            'Call',
            'Applicant',
            'Gender',
            'Email',
            'Home Institute',
            'Proposed Start',
            'Host Institute',
            'Proposed End',
            
            
        ]
        # Write some data headers.
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Start from the first cell below the headers.
        row = 1
        col = 0
        
      
        fellowship_applications = self.get_queryset()
        # Iterate over the data and write it out row by row.
        for application in fellowship_applications:
            fields = [
                application.call.call_id,
                application.user.first_name +" "+ application.user.last_name,
                application.user.get_gender_display(),
                application.user.business_email,
                application.home_institute_name,
                application.host_institute_name,
                application.proposed_begining,
                application.proposed_end,
             
            ]
            for col, field in enumerate(fields):
                worksheet.write(row, col, field)
                worksheet.set_column('H:H', None, date_format)
                worksheet.set_column('G:G', None, date_format)
                
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
            return self.export_excel_report(request, context)
        return self.render_to_response(context)



class FellowshipapplicationsValidationListView(LoginRequiredMixin, TemplateView):
    model = Fellowshipapplication
    context_object_name = "applications_list"
    template_name = "fellowship_validation_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(status='submitted')
        '''
        if not self.request.user.has_perm('fellowship_applications.change_fellowshipapplication') and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user.id)
        '''
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in = self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('applicant_name'))|
                    Q(user__last_name__icontains=request_post.get('applicant_name')))
            if request_post.get('status'):
                queryset = queryset.filter(
                    state=request_post.get('state'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationsValidationListView, self).get_context_data(**kwargs)
        context["fellowship_applications"] = self.get_queryset().order_by()
        context["states"] = Fellowshipapplication.APPLICATION_STATES
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
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)




class CreateFellowshipapplicationView(LoginRequiredMixin, CreateView):
    model = Fellowshipapplication
    form_class = FellowshipapplicationForm
    template_name = "create_fellowship_application.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateFellowshipapplicationView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFellowshipapplicationView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            #print(self.profile_form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        try:

        #with transaction.atomic():
            application = form.save(commit=False)

            application.user = self.request.user
            application.save()
            application.state = 'submitted'
            application.save()
            #sending email to the applicant after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Fellowship Application'
            message = render_to_string('fellowship_application_confirmation_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': application
            })
            email = EmailMessage(mail_subject, message, to=[self.request.user.business_email],from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()


            if self.request.POST.get("savenewform"):
                return redirect("fellowship_applications:list")

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                'fellowship_applications:list'), 'error': False}
                return JsonResponse(data)
            messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application Submitted successfully.')
            return redirect("fellowship_applications:list")
        except IntegrityError:
            messages.add_message(self.request, messages.WARNING, 'You can not apply more than once for the same call.')
            return redirect("fellowship_applications:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_initial(self, *args, **kwargs):
        initial = super(CreateFellowshipapplicationView, self).get_initial(**kwargs)
        initial['call'] = FellowshipCall.objects.get(pk=self.kwargs['call_pk'])
        user = self.request.user
        initial.update({
            'title': user.title,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'country': user.country,
            'nationality': user.nationality,
            'mobile':user.mobile,
            'business_tel':user.business_tel,
            'area_of_specialisation':user.area_of_specialisation,
            'business_address':user.business_address,
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateFellowshipapplicationView, self).get_context_data(**kwargs)
        context["form"] = context["form"]
        context['calls'] = FellowshipCall.objects.filter(
            submission_deadline__gte=datetime.date.today()
        )
        user = self.request.user

        initial = {
            'title': user.title,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'country': user.country,
            'nationality': user.nationality,
            'mobile': user.mobile,
            'business_tel': user.business_tel,
            'business_address': user.business_address,
            'institution': user.institution
        }
        return context


#Fellowships application details
class FellowshipapplicationDetailView(LoginRequiredMixin, DetailView):
    model = Fellowshipapplication
    context_object_name = "application_record"
    template_name = "view_fellowship_application.html"

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationDetailView, self).get_context_data(**kwargs)
        application_record = context["application_record"]
        
        context.update({
            "reviews": application_record.reviews.all(),
            "review_form": FellowshipappreviewForm()
        })
        return context



#SalesAccessRequiredMixin,
class FellowshipapplicationUpdateView( LoginRequiredMixin, UpdateView):
    model = Fellowshipapplication
    form_class = FellowshipapplicationForm
    template_name = "create_fellowship_application.html"

    def dispatch(self, request, *args, **kwargs):

        return super(FellowshipapplicationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FellowshipapplicationUpdateView, self).get_form_kwargs()
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
        # Save Fellowshipapplication
        with transaction.atomic():
            application = form.save(commit=False)
            if 'savefinal' in self.request.POST:
                print("will save final")
                application.state = 'submitted'
            else:
                print("save draft")
            application.save()
            form.save_m2m()

        if self.request.POST.get("savenewform"):
            return redirect("fellowship_applications:list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'fellowship_applications:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application updated successfully.')
        return redirect("fellowship_applications:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationUpdateView, self).get_context_data(**kwargs)
        context["applicationobj"] = self.object
        user = self.request.user

        return context


# assign fellowship application reviewers
class FellowshipapplicationReviewersView(LoginRequiredMixin, TemplateView):
    model = Fellowshipapplication
    context_object_name = "applications_list"
    form_class = FellowshipapplicationReviewersForm
    template_name = "assign_fellowship_reviewers.html"

    def get_queryset(self):
        status = ['validated', ]
        queryset = self.model.objects.filter(
            status__in=status, reviewers=self.request.user
        ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status__in=status).order_by('-id')

        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in=self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('applicant_name')) |
                    Q(user__last_name__icontains=request_post.get('applicant_name')))
            if request_post.get('proposal_title'):
                queryset = queryset.filter(
                    Q(proposal_title__icontains=request_post.get('proposal_title')))

            if request_post.get('call_id'):
                queryset = queryset.filter(
                    Q(call__call_id__icontains=request_post.get('call_id')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["grants_applications"] = self.get_queryset()

        context["per_page"] = self.request.POST.get('per_page')

        context["applicationform"] = FellowshipapplicationReviewersForm

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



#SalesAccessRequiredMixin,
class FellowshipapplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Fellowshipapplication
    template_name = 'view_account.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("fellowship_applications:list")


class AddFellowshipappreviewView(LoginRequiredMixin, CreateView):
    model = Fellowshipappreview
    form_class = FellowshipappreviewForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.application = get_object_or_404(
            Fellowshipapplication, id=request.POST.get('applicationid'))
       
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

        data = {
            'error': "You don't have permission to review for this account."}
        return JsonResponse(data)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.reviewer = self.request.user
        review.application = self.application
        review.date = timezone.now()
        review.save()
        review_id = review.id
        current_site = get_current_site(self.request)
        # ToDo: send an email to the reviewer
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'fellowship_applications:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application Reviewed successfully.')
        return redirect("fellowship_applications:list")

    def form_invalid(self, form):
        print(form.errors)
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return JsonResponse({"error": form.errors})


class UpdateFellowshipappreviewView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.review_obj = get_object_or_404(
            Fellowshipappreview, id=request.POST.get("reviewid"))
        if request.user == self.review_obj.reviewed_by:
            form = FellowshipapplicationFellowshipappreviewForm(request.POST, instance=self.review_obj)
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        data = {'error': "You don't have permission to edit this review."}
        return JsonResponse(data)

    def form_valid(self, form):
        self.review_obj.review = form.cleaned_data.get("review")
        self.review_obj.save(update_fields=["review"])
        review_id = self.review_obj.id
        current_site = get_current_site(self.request)
        send_email_user_mentions.delay(review_id, 'applications', domain=current_site.domain,
            protocol=self.request.scheme)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application Review Updated successfully.')
        return JsonResponse({
            "review_id": self.review_obj.id,
            "review": self.review_obj.review,
        })

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return JsonResponse({"error": form['review'].errors})


class DeleteFellowshipappreviewView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Fellowshipappreview, id=request.POST.get("review_id"))
        if request.user == self.object.reviewed_by:
            self.object.delete()
            data = {"cid": request.POST.get("review_id")}
            return JsonResponse(data)

        data = {'error': "You don't have permission to delete this review."}
        return JsonResponse(data)



#  Application review Form
class FellowshipapplicationReview(LoginRequiredMixin, DetailView):
    model = Fellowshipapplication
    context_object_name = "application_record"
    template_name = "view_fellowship_application.html"

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationReview, self).get_context_data(**kwargs)
        application_record = context["application_record"]
        
        context.update({
            #"reviews": application_record.fellowship_reviews.all(),
            "review_form": FellowshipappreviewForm()
        })
        return context



# select call before applying for a fellowship
class SelectCallView(LoginRequiredMixin, CreateView):
    model = Fellowshipapplication
    form_class = SelectCallForm
    template_name = "select_fellowship_application_call.html"

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
        return redirect("fellowship_applicationss:add_application", call.pk)
        

    def form_invalid(self, form, other_form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(SelectCallView, self).get_context_data(**kwargs)
        print("context", context, "kwargs", kwargs)
        return context

#Assign Fellowship Validators
class FellowshipapplicationValidatorsView(LoginRequiredMixin, TemplateView):
    model = Fellowshipapplication
    context_object_name = "applications_list"
    form_class = FellowshipapplicationValidatorsForm
    template_name = "assig_fellowship_validators.html"

    def get_queryset(self):
        status = ['submitted']  # do we need 'noncompliant' to be reviewed too?
        queryset = self.model.objects.filter(
            status__in=status, reviewers=self.request.user, reviews__isnull=True
        ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status='submitted').order_by('-id')

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('applicant_name')) |
                    Q(user__last_name__icontains=request_post.get('applicant_name')))
            if request_post.get('proposal_title'):
                queryset = queryset.filter(
                    Q(proposal_title__icontains=request_post.get('proposal_title')))

            if request_post.get('call_id'):
                queryset = queryset.filter(
                    Q(call__call_id__icontains=request_post.get('call_id')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["fellowship_applications"] = self.get_queryset()

        context["per_page"] = self.request.POST.get('per_page')

        context["applicationform"] = FellowshipapplicationValidatorsForm

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


# assign fellowship validators post method
class AssignFellowshipValidatorsView(LoginRequiredMixin, TemplateView):
    template_name = "assig_fellowship_validators.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssignFellowshipValidatorsView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssignFellowshipValidatorsView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = FellowshipapplicationValidatorsForm(request.POST, request=request)
        if form.is_valid():
            grant_applications_ids = request.POST.getlist('application')
            list_of_obj = Fellowshipapplication.objects.filter(pk__in=grant_applications_ids)
            list_of_validators = request.POST.getlist('validators')
            users_who_are_validators = User.objects.filter(pk__in=list_of_validators)
            for application in list_of_obj:
                form.save(commit=False)
                application.fellowship_manager = self.request.user
                application.save()
                for validator in list_of_validators:
                    try:
                        application.validators.add(validator)
                    except IntegrityError:
                        try:
                            application.validators.add(validator)
                        except IntegrityError:
                            continue

            for user in users_who_are_validators:
                current_site = get_current_site(self.request)
                subject = 'Fellowship Application Validation Request'
                message = render_to_string('fellowship_application_validation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'applications': list_of_obj
                })
                user.email_user(subject, message)
            # sending email to the  grants manager after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Fellowship Application Validation Request'
            message = render_to_string('send_validator_fellowship_application_email_grants_manager.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'applications': list_of_obj,
                'validators': application.validators.all()

            })
            email = EmailMessage(mail_subject, message, to=[self.request.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                        'fellowship_applicationss:list'), 'error': False}
                return redirect("fellowship_applicationss:list")
            messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application Validator assigned  successfully.')
            return redirect("fellowship_applicationss:list")

#Fellowship application viewset
class FellowshipApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants applications to be viewed or edited.
    """

    serializer_class = FellowshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','country','email_1']
    ordering_fields = ['call__call_id','first_name','country','email_1']

    def get_queryset(self):
        queryset = Fellowshipapplication.objects.filter(user=self.request.user.id).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Fellowshipapplication.objects.filter(status='Submitted').order_by('-id')

        return queryset.distinct()

class FellowshipApplicationValidationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants applications to be validated or edited.
    """

    serializer_class = FellowshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country']
    ordering_fields = ['call__call_id','first_name','last_name','country',]

    def get_queryset(self):
        queryset = Fellowshipapplication.objects.filter(status='Submitted', validators=self.request.user).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Fellowshipapplication.objects.filter(status='Submitted').order_by('-id')

        return queryset.distinct()

class FellowshipapplicationValidateView(LoginRequiredMixin, UpdateView):
    model = Fellowshipapplication
    form_class = FellowshipapplicationValidateForm
    template_name = "validate_fellowship_application.html"

    def dispatch(self, request, *args, **kwargs):
       
        return super(FellowshipapplicationValidateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FellowshipapplicationValidateView, self).get_form_kwargs()
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
            applicationobject.status = 'validated'
        else:
            applicationobject.status = 'noncompliant'
        applicationobject.save()
        if applicationobject.status =='validated':
            # send successful message to the applicant
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Fellowship Application Compliancy '
            message = render_to_string('fellowship_application_compliance_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': applicationobject
            })
            email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()
        if applicationobject.status =='noncompliant':
            # send successful message to the applicant
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Fellowship Application Compliancy'
            message = render_to_string('grant_fellowship_noncompliant_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': applicationobject
            })
            email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application Validated  successfully.')
        return redirect("fellowship_applicationss:validation_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationValidateView, self).get_context_data(**kwargs)
        context["application_record"] = self.object
        context["form"] = context["form"]
      
        return context

class ValidatedFellowshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows fellowships applications to be validated or edited.
    """

    serializer_class = FellowshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country']
    ordering_fields = ['call__call_id','first_name','last_name','country',]

    def get_queryset(self):
        queryset = Fellowshipapplication.objects.filter(reviewers = self.request.user
           ,status='validated',validators=self.request.user).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Fellowshipapplication.objects.filter(status='validated').order_by('-id')

        return queryset.distinct()


# Fellowship review list 
class FellowshipapplicationsReviewListView(LoginRequiredMixin, TemplateView):
    model = Fellowshipapplication
    context_object_name = "applications_list"
    template_name = "fellowship_review_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(status='validated')
    
        if not self.request.user.has_perm('fellowship_applications.change_fellowshipapplication') and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user.id,status='validated')
      
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationsReviewListView, self).get_context_data(**kwargs)
        context["fellowship_applications"] = self.get_queryset().order_by()
        context["per_page"] = self.request.POST.get('per_page')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

# save fellowship reviewers
class SaveFellowshipapplicationReviewersView(LoginRequiredMixin, UpdateView):
    template_name = "assign_fellowship_reviewers.html"

    def dispatch(self, request, *args, **kwargs):
        return super(SaveFellowshipapplicationReviewersView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SaveFellowshipapplicationReviewersView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = FellowshipapplicationReviewersForm(request.POST)

        if form.is_valid():
            grant_applications_ids = request.POST.getlist('application')
            list_of_obj = Fellowshipapplication.objects.filter(pk__in=grant_applications_ids)
            list_of_reviewers = request.POST.getlist('reviewers')
            users_who_are_reviewers = User.objects.filter(pk__in=list_of_reviewers)
            for application in list_of_obj:
                form.save(commit=False)
                application.grant_manager = self.request.user
                application.save()
                for reviewer in list_of_reviewers:
                    try:
                        application.reviewers.add(reviewer)
                    except IntegrityError:
                        try:
                            application.reviewers.add(reviewer)
                        except IntegrityError:
                            continue

            for user in users_who_are_reviewers:
                current_site = get_current_site(self.request)
                subject = 'Fellowship application Review Request'
                message = render_to_string('fellowship_application_review_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'applications': list_of_obj
                })
                user.email_user(subject, message)

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                        'fellowship_applicationss:list'), 'error': False}
                return redirect("fellowship_applicationss:list")
            messages.add_message(self.request, messages.SUCCESS, 'Fellowship Application reviewers assigned  successfully.')
            return redirect("fellowship_applicationss:list")


class ReviewedViewSet(viewsets.ModelViewSet):
  
    serializer_class = FellowshipApplicationReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country','home_institute_name','host_institute_name']
    ordering_fields = ['call__call_id','first_name','last_name','country','home_institute_name','host_institute_name']

    def get_queryset(self):
        #status = ['rejected', 'selected_for_funding']  # do we need 'noncompliant' to be reviewed too?
        queryset = Fellowshipapplication.objects.filter(
             reviewers=self.request.user, reviews__isnull=False
            ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Fellowshipapplication.objects.filter( reviews__isnull=False).distinct().order_by('-id')
        
        return queryset.distinct()

# Fellowship reviewed list 
class FellowshipapplicationsReviewedListView(LoginRequiredMixin, TemplateView):
    model = Fellowshipapplication
    context_object_name = "applications_list"
    template_name = "fellowship_reviewed_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(reviews__isnull=False)
    
        if not self.request.user.has_perm('fellowship_applications.change_fellowshipapplication') and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user.id, reviews__isnull=False)
      
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationsReviewedListView, self).get_context_data(**kwargs)
        context["fellowship_applications"] = self.get_queryset().order_by('-id')
        context["per_page"] = self.request.POST.get('per_page')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


#Fellowships application details
class FellowshipapplicationDecisionView(LoginRequiredMixin, DetailView):
    model = Fellowshipapplication
    context_object_name = "application_record"
    template_name = "decision_view.html"

    def get_context_data(self, **kwargs):
        context = super(FellowshipapplicationDecisionView, self).get_context_data(**kwargs)
        application_record = context["application_record"]
        
        context.update({
            "reviews": application_record.reviews.all(),
            "review_form": FellowshipappreviewForm(),
            "average_score": application_record.reviews.all().aggregate(Avg('score'))
        })
        return context
