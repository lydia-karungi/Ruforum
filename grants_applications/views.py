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

from common.choices import COUNTRY_CHOICES
from .models import Grantapplication, Grantappreview, Collaborator, Supportingletter, ProjectBudget
from contacts.models import User
from calls.models import GrantCall
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import transaction
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from contacts.models import User
from django.db.models import Avg
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import EmailMessage
from .serializers import GrantApplicationSerializer,GrantApplicationReviewSerializer

from .forms import (
    GrantProfileForm, GrantapplicationForm, CollaboratorFormSet,
    SupportingletterFormSet, GrantappreviewForm,
    GrantapplicationValidateForm, GrantapplicationReviewersForm, GrantCarpappreviewForm
, SelectCallForm, GrantapplicationUpdateForm, GrantapplicationValidatorsForm, GrantapplicationRejectForm
)
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters


# Display list of grant applications
class GrantapplicationsListView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    template_name = "applications.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user.id).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status='submitted').order_by('-id')
            print(queryset)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationsListView, self).get_context_data(**kwargs)
        context["grants_applications"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

  

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class GrantapplicationsValidationListView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    template_name = "validation_list.html"

    def get_queryset(self):
      
        queryset = self.model.objects.filter(
            status='submitted', validators=self.request.user
        ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status='submitted').order_by('-id')
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationsValidationListView, self).get_context_data(**kwargs)
        context["grants_applications"] = self.get_queryset().order_by('-last_modified')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    # validated grant applications


class GrantapplicationsValidatedListView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    template_name = "validated_list.html"

    def get_queryset(self):
        # queryset = self.model.objects.filter(state='submitted')
        queryset = self.model.objects.filter(
            status='validated', validators=self.request.user
        ).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.order_by('-id')

        request_post = self.request.POST
        if request_post:
            if request_post.get('applicant_name'):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=request_post.get('applicant_name')) |
                    Q(user__last_name__icontains=request_post.get('applicant_name')))
          
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationsValidatedListView, self).get_context_data(**kwargs)
        context["grants_applications"] = self.get_queryset().order_by('-last_modified')
        context["states"] = Grantapplication.APPLICATION_STATES
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

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class GrantapplicationsReviewListView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    template_name = "review_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(reviewers = self.request.user
           ,status='validated').exclude(reviews__reviewer=self.request.user).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status='validated', reviews__isnull=True).order_by('-id')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationsReviewListView, self).get_context_data(**kwargs)

        context["grants_applications"] = self.get_queryset().order_by('-last_modified')
        context["states"] = Grantapplication.APPLICATION_STATES

        context["per_page"] = self.request.POST.get('per_page')
     
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateGrantapplicationView(LoginRequiredMixin, CreateView):
    model = Grantapplication
    form_class = GrantapplicationForm
    template_name = "create_application.html"

    def dispatch(self, request, *args, **kwargs):
        self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateGrantapplicationView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateGrantapplicationView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        # removing the profile form
        # self.grantapplication_form = GrantProfileForm(request.POST, request.FILES)
        self.collaborators = CollaboratorFormSet(request.POST, request.FILES, prefix='collaborator_set')
        self.supporting_letters = SupportingletterFormSet(request.POST, request.FILES, prefix='supportingletter_set')

        formsets_valid = (
                self.collaborators.is_valid() and self.supporting_letters.is_valid()
        )
        # removed validation for profile form -->and self.profile_form.is_valid()
        if form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            # print(self.profile_form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        try:

            # Save Grantapplication
            # context = self.get_context_data()
            # collaborators = context['collaborators']

            # with transaction.atomic():
            application = form.save(commit=False)

            application.user = self.request.user
            # profile = self.profile_form.save()
            # application.last_name = profile.last_name
            # application.department = profile.department
            # application.highest_qualification = profile.highest_qualification
            # application.area_of_specialisation = profile.area_of_specialisation
            # application.cv = profile.cv
            application.save()
            # form.save_m2m()

            self.collaborators.instance = application
            self.collaborators.save()
            self.supporting_letters.instance = application
            self.supporting_letters.save()
            application.status = 'submitted'
            application.save()
            # sending email to the applicant after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grant Application'
            message = render_to_string('grant_application_confirmation_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': application
            })
            email = EmailMessage(mail_subject, message, to=[self.request.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

            if self.request.POST.get("savenewform"):
                return redirect("grants_applications:list")

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                    'grants_applications:list'), 'error': False}
                return JsonResponse(data)

            messages.add_message(self.request, messages.SUCCESS, 'Grant Application Submitted successfully.')
            return redirect("grants_applications:list")
        except IntegrityError:
            messages.add_message(self.request, messages.WARNING, 'You can not apply more than once for the same call.')
            return redirect("grants_applications:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form,
                                  collaborators=self.collaborators, supporting_letters=self.supporting_letters)
        )

    def get_initial(self, *args, **kwargs):
        initial = super(CreateGrantapplicationView, self).get_initial(**kwargs)
        initial['call'] = GrantCall.objects.get(pk=self.kwargs['call_pk'])
        user = self.request.user
        initial.update({
            'title': user.title,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'country': user.country,
            'nationality': user.nationality,
            'mobile': user.mobile,
            'business_tel': user.business_tel,
            'area_of_specialisation': user.area_of_specialisation,
            'email': user.business_email,
            'business_address': user.business_address,
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateGrantapplicationView, self).get_context_data(**kwargs)
        context["form"] = context["form"]
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
            'institution': user.institution,
            'email': user.business_email
        }
        context["profile_form"] = context.get('profile_form') or GrantProfileForm(initial=initial)
        context['calls'] = GrantCall.objects.filter(
            grant_type__isnull=False,
            submission_deadline__gte=datetime.date.today()
        )
        context['call'] = GrantCall.objects.get(pk=self.kwargs['call_pk'])
        context["users"] = self.users
        context['collaborator_formset'] = context.get('collaborators') or CollaboratorFormSet(prefix='collaborator_set')
        context['letter_formset'] = context.get('supporting_letters') or SupportingletterFormSet(
            prefix='supportingletter_set')

        return context


# Grants application details
class GrantapplicationDetailView(LoginRequiredMixin, DetailView):
    model = Grantapplication
    context_object_name = "application_record"
    template_name = "view_application.html"

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationDetailView, self).get_context_data(**kwargs)
        application_record = context["application_record"]
        cvs = Collaborator.objects.filter(application=application_record)
        context['collaborators'] = cvs
        context["supportletters"] = Supportingletter.objects.filter(application=application_record)
        '''
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != applicationrecord.user:
                raise PermissionDenied
        '''
        review_permission = True if (
                self.request.user == application_record.user or
                self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        context.update({
            "reviews": application_record.reviews.all(),
            "review_form": GrantappreviewForm(),
            "average_score": application_record.reviews.all().aggregate(Avg('score'))

        })
        return context


class GrantapplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Grantapplication
    form_class = GrantapplicationUpdateForm
    template_name = "edit_grant_application.html"

    def dispatch(self, request, *args, **kwargs):
        '''
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
        elif request.user.google.all():
            self.users = []
        else:
            self.users = User.objects.filter(role='ADMIN').order_by('email')
        '''
        return super(GrantapplicationUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GrantapplicationUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        # self.profile_form = GrantProfileForm(request.POST, request.FILES, instance=request.user)
        self.collaborators = CollaboratorFormSet(request.POST, request.FILES, instance=self.object,
                                                 prefix='collaborator_set')
        self.supporting_letters = SupportingletterFormSet(request.POST, request.FILES, instance=self.object,
                                                          prefix='supportingletter_set')

        formsets_valid = (
                self.collaborators.is_valid() and self.supporting_letters.is_valid()
        )
        if form.is_valid() and formsets_valid:
            return self.form_valid(form)
        else:
            print(form.errors)
            # print(self.profile_form.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Grantapplication
        with transaction.atomic():
            application = form.save(commit=False)
            if 'savefinal' in self.request.POST:
                print("will save final")
                application.status = 'submitted'
            else:
                print("save draft")
            application.save()
            # form.save_m2m()

            self.collaborators.instance = application
            self.collaborators.save()
            self.supporting_letters.instance = application
            self.supporting_letters.save()

        if self.request.POST.get("savenewform"):
            return redirect("grants_applications:list")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grants_applications:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant Application updated successfully.')

        return redirect("grants_applications:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form,
                                  collaborators=self.collaborators, supporting_letters=self.supporting_letters)
        )

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationUpdateView, self).get_context_data(**kwargs)
        context["applicationobj"] = self.object
        user = self.request.user
        context['calls'] = GrantCall.objects.filter(
            grant_type__isnull=False,
            submission_deadline__gte=datetime.date.today()
        )

        context['collaborator_formset'] = context.get('collaborators') or CollaboratorFormSet(instance=self.object,
                                                                                              prefix='collaborator_set')
        context['letter_formset'] = context.get('supporting_letters') or SupportingletterFormSet(instance=self.object,
                                                                                                 prefix='supportingletter_set')

        return context


# assign grants validators
class GrantapplicationValidatorsView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    form_class = GrantapplicationValidatorsForm
    template_name = "assign_validators.html"

    def get_queryset(self):
        status = ['submitted']  # do we need 'noncompliant' to be reviewed too?
        queryset = self.model.objects.filter(
            status__in=status, reviewers=self.request.user, reviews__isnull=True
        ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status='submitted').order_by('-id')

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

        context["applicationform"] = GrantapplicationValidatorsForm

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


class GrantapplicationValidateView(LoginRequiredMixin, UpdateView):
    model = Grantapplication
    form_class = GrantapplicationValidateForm
    template_name = "validate_application.html"

    def dispatch(self, request, *args, **kwargs):
       
        return super(GrantapplicationValidateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GrantapplicationValidateView, self).get_form_kwargs()
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
            mail_subject = 'Ruforum Grant Application Compliancy '
            message = render_to_string('grant_application_compliance_email.html', {
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
            mail_subject = 'Ruforum Grant Application Compliancy'
            message = render_to_string('grant_application_noncompliant_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': applicationobject
            })
            email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()

        messages.add_message(self.request, messages.SUCCESS, 'Grant Application Validated  successfully.')
        return redirect("grants_applications:validation_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationValidateView, self).get_context_data(**kwargs)
        context["application_record"] = self.object
        cvs = Collaborator.objects.filter(application=self.object)
        context['collaborators'] = cvs
        context["supportletters"] = Supportingletter.objects.filter(application=self.object)
        context["applicationform"] = context["form"]
        return context


# SalesAccessRequiredMixin,
class GrantapplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Grantapplication
    template_name = 'view_account.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("grants_applications:list")


class AddGrantappreviewView(LoginRequiredMixin, CreateView):
    model = Grantappreview
    form_class = GrantappreviewForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.application = get_object_or_404(Grantapplication, id=request.POST.get('application'))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

        data = {
            'error': "You don't have permission to review for this account."}
        return JsonResponse(data)

    def form_valid(self, form):
        try:

            review = form.save(commit=False)
            review.reviewer = self.request.user
            review.application = self.application
            review.date = timezone.now()
            review.save()
            review_id = review.id
            # sending email to the reviewer and grants manager after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Ruforum Grant Application Review'
            message = render_to_string('send_review_grant_application_email.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'application': review.application,
                'grants_manager': review.application.grant_manager

            })
            email = EmailMessage(mail_subject, message, to=[self.request.user.business_email],
                                 from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()
            # sending email to the  grants manager after submission
            if review.application.grant_manager is not None and self.request.user is not review.application.grant_manager:
                current_site = get_current_site(self.request)
                mail_subject = 'Ruforum Grant Application Review'
                message = render_to_string('send_review_grant_application_email_grants_manager.html', {
                    'user': self.request.user,
                    'domain': current_site.domain,
                    'application': review.application,
                    'grants_manager': review.application.grant_manager

                })
                email = EmailMessage(mail_subject, message, to=[review.application.grant_manager.business_email],
                                 from_email="nonereply@ruforum.org")
                email.content_subtype = "html"
                email.send()
            messages.add_message(self.request, messages.SUCCESS, 'Grant Application Review was added successfully.')
            return JsonResponse({
                "message": review.id,

            })
        except IntegrityError:

            return JsonResponse({"errormessage": "You can not review the same application more than once!"})

    def form_invalid(self, form):
        print(form.errors)
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return JsonResponse({"error": form.errors})


class UpdateGrantappreviewView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.review_obj = get_object_or_404(
            Grantappreview, id=request.POST.get("reviewid"))
        if request.user == self.review_obj.reviewed_by:
            form = GrantapplicationGrantappreviewForm(request.POST, instance=self.review_obj)
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
        messages.add_message(self.request, messages.SUCCESS, 'Grant Application Review was updated successfully.')
        return JsonResponse({
            "review_id": self.review_obj.id,
            "review": self.review_obj.review,
        })

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return JsonResponse({"error": form['review'].errors})


class DeleteGrantappreviewView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Grantappreview, id=request.POST.get("review_id"))
        if request.user == self.object.reviewed_by:
            self.object.delete()
            data = {"cid": request.POST.get("review_id")}
            return JsonResponse(data)

        data = {'error': "You don't have permission to delete this review."}
        return JsonResponse(data)


# reviewed list of grants applications
class GrantapplicationsReviewedListView(LoginRequiredMixin, TemplateView):
    model = Grantappreview
    context_object_name = "applications_list"
    template_name = "reviewed_list.html"

    def get_queryset(self):
        queryset = Grantapplication.objects.filter(
             reviewers=self.request.user, reviews__isnull=False
            ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Grantapplication.objects.filter( reviews__isnull=False).distinct().order_by('-id')


        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["grants_applications"] = self.get_queryset()
        context["states"] = Grantappreview.RECOMMENDATIONS

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# grant Application review Form
class GrantapplicationReview(LoginRequiredMixin, DetailView):
    model = Grantapplication
    context_object_name = "application_record"
    template_name = "Review_application.html"

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationReview, self).get_context_data(**kwargs)
        application_record = context["application_record"]
        cvs = Collaborator.objects.filter(application=application_record)
        context['collaborators'] = cvs
        context["supportletters"] = Supportingletter.objects.filter(application=application_record)
        context['review_form'] = GrantCarpappreviewForm()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            context['reviews'] = application_record.reviews.all()
        context['reviews'] = application_record.reviews.filter(reviewer =self.request.user)
        return context


# Carp+ Application review Form
class GrantCarpapplicationReview(LoginRequiredMixin, CreateView):
    model = Grantappreview
    form_class = GrantCarpappreviewForm
    template_name = "Review_carp_application.html"

    def dispatch(self, request, *args, **kwargs):
        return super(GrantCarpapplicationReview, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GrantCarpapplicationReview, self).get_form_kwargs()
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
        # Save form
        review = form.save(commit=False)
        review.reviewer = self.request.user
        review.date = timezone.now()
        review.save()

        if self.request.POST.get("savenewform"):
            return redirect("grants_applicationss:review_carp_application")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grants_applicationss:reviewed_list'), 'error': False}

            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant Application Review was added successfully.')
        return redirect("grants_applicationss:reviewed_list")

    def form_invalid(self, form):
        print(form.errors)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(GrantCarpapplicationReview, self).get_context_data(**kwargs)
        context["form"] = context["form"]
        context['application_id'] = self.kwargs['pk']

        return context


# select call before applying for a grant
class SelectCallView(LoginRequiredMixin, CreateView):
    model = Grantapplication
    form_class = SelectCallForm
    template_name = "select_grant_application_call.html"

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
        return redirect("grants_applicationss:add_application", call.pk)

    def form_invalid(self, form, other_form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(SelectCallView, self).get_context_data(**kwargs)
        print("context", context, "kwargs", kwargs)
        return context


class GrantapplicationRejectView(LoginRequiredMixin, UpdateView):
    model = Grantapplication
    form_class = GrantapplicationRejectForm
    template_name = "validate_application.html"

    def dispatch(self, request, *args, **kwargs):

        return super(GrantapplicationRejectView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GrantapplicationRejectView, self).get_form_kwargs()
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
        applicationobject.selected_for_funding = False
        applicationobject.status = 'rejected'
        applicationobject.save()
        # sending email to the rejected applicant

        current_site = get_current_site(self.request)
        mail_subject = 'Ruforum Grant Application'
        message = render_to_string('grant_reject_email.html', {
                'user': applicationobject.user,
                'domain': current_site.domain,
                'application': applicationobject

        })
        email = EmailMessage(mail_subject, message, to=[applicationobject.user.business_email],from_email="nonereply@ruforum.org")
        email.content_subtype = "html"
        email.send()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grants:list'), 'error': False}
            return JsonResponse({'success_message': "Application Rejected" })
        messages.add_message(self.request, messages.SUCCESS, 'Grant Application Rejected.')
        redirect("grants_applicationss:application_decision_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationRejectView, self).get_context_data(**kwargs)
        context["applicationobj"] = self.object
        application_record = context["applicationobj"]

        context["applicationform"] = context["form"]
        return context


# grant application decision
class GrantapplicationsDecisionListView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    template_name = "application_decision_list.html"

    def get_queryset(self):
        status = ['rejected', 'selected_for_funding']  # do we need 'noncompliant' to be reviewed too?
        queryset = self.model.objects.filter(
            status__in=status, reviewers=self.request.user
        ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.filter(status__in=status).distinct().order_by('-id')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["grants_applications"] = self.get_queryset()
    
        return context




# assign grants validators post method
class AssignValidatorsView(LoginRequiredMixin, TemplateView):
    template_name = "assign_validators.html"

    def dispatch(self, request, *args, **kwargs):
        return super(AssignValidatorsView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssignValidatorsView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = GrantapplicationValidatorsForm(request.POST, request=request)
        if form.is_valid():
            grant_applications_ids = request.POST.getlist('application')
            list_of_obj = Grantapplication.objects.filter(pk__in=grant_applications_ids)
            list_of_validators = request.POST.getlist('validators')
            users_who_are_validators = User.objects.filter(pk__in=list_of_validators)
            for application in list_of_obj:
                form.save(commit=False)
                application.grant_manager = self.request.user
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
                subject = 'Grant Application Validation Request'
                message = render_to_string('grant_application_validation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'applications': list_of_obj
                })
                user.email_user(subject, message)
            # sending email to the  grants manager after submission
            current_site = get_current_site(self.request)
            mail_subject = 'Grant Application Validation Request'
            message = render_to_string('send_validator_grant_application_email_grants_manager.html', {
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
                        'grants_applications:list'), 'error': False}
                return redirect("grants_applications:list")
            messages.add_message(self.request, messages.SUCCESS, 'Grant Application Validator assigned  successfully.')
            return redirect("grants_applications:list")


# assign grants reviewers
class AssignGrantReviewersListView(LoginRequiredMixin, TemplateView):
    model = Grantapplication
    context_object_name = "applications_list"
    form_class = GrantapplicationReviewersForm
    template_name = "assign_reviewers.html"

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

        context["applicationform"] = GrantapplicationReviewersForm

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


class GrantapplicationReviewersView(LoginRequiredMixin, UpdateView):
    template_name = "assign_reviewers.html"

    def dispatch(self, request, *args, **kwargs):
        return super(GrantapplicationReviewersView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GrantapplicationReviewersView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        form = GrantapplicationReviewersForm(request.POST, request=request)

        if form.is_valid():
            grant_applications_ids = request.POST.getlist('application')
            list_of_obj = Grantapplication.objects.filter(pk__in=grant_applications_ids)
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
                subject = 'Grant application Review Request'
                message = render_to_string('grant_application_review_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'applications': list_of_obj
                })
                user.email_user(subject, message)

            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                        'grants_applications:list'), 'error': False}
                return redirect("grants_applications:list")
            messages.add_message(self.request, messages.SUCCESS, 'Grant Application reviewers assigned  successfully.')
            return redirect("grants_applications:list")


class GrantApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants applications to be viewed or edited.
    """

    serializer_class = GrantApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']
    ordering_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']

    def get_queryset(self):
        queryset = Grantapplication.objects.filter(user=self.request.user.id).order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Grantapplication.objects.filter(status='submitted').order_by('-id')

        return queryset.distinct()


class GrantApplicationValidationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants applications to be validated or edited.
    """

    serializer_class = GrantApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']
    ordering_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']

    def get_queryset(self):
        queryset = Grantapplication.objects.filter(status='submitted', validators=self.request.user).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Grantapplication.objects.filter(status='submitted').order_by('-id')

        return queryset.distinct()


class GrantApplicationDecisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants applications to be validated or edited.
    """

    serializer_class = GrantApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']
    ordering_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']

    def get_queryset(self):
        status = ['rejected', 'selected_for_funding']  # do we need 'noncompliant' to be reviewed too?
        queryset = Grantapplication.objects.filter(
            status__in=status, reviewers=self.request.user
            ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Grantapplication.objects.filter(status__in=status).distinct().order_by('-id')
        
        return queryset.distinct()

class ReviewedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants applications to be validated or edited.
    """

    serializer_class = GrantApplicationReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']
    ordering_fields = ['call__call_id','first_name','last_name','country','proposal','gender','email','nationality','total_budget','last_modified']

    def get_queryset(self):
        #status = ['rejected', 'selected_for_funding']  # do we need 'noncompliant' to be reviewed too?
        queryset = Grantapplication.objects.filter(
             reviewers=self.request.user, reviews__isnull=False
            ).distinct().order_by('-id')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = Grantapplication.objects.filter( reviews__isnull=False).distinct().order_by('-id')
        
        return queryset.distinct()