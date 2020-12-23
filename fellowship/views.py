from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)
from common.utils import has_group
from fellowship.models import Fellowship, FellowshipComment
from fellowship_applications.models import Fellowshipapplication
from contacts.models import User
from django.urls import reverse_lazy, reverse
from navutils import MenuMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site

from .forms import FellowshipForm, FellowshipCommentForm,FellowshipTypeForm
import datetime
from calls.models import FellowshipType
import logging
log = logging.getLogger('RIMS')

class FellowshipsListView(LoginRequiredMixin, TemplateView):
    model = Fellowship
    context_object_name = "fellowship_list"
    template_name = "fellowship.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in = self.request.GET.getlist('tag'))

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

            if request_post.get('fellowship_id'):
                queryset = queryset.filter(
                    fellowship_id__icontains=request_post.get('fellowship_id'))
            if request_post.get('title'):
                queryset = queryset.filter(
                    title__contains=request_post.get('title'))
            if request_post.get('call'):
                queryset = queryset.filter(
                    call__title__icontains=request_post.get('call'))
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
        context = super(FellowshipsListView, self).get_context_data(**kwargs)
        fellowship_applications = Fellowshipapplication.objects.all()
        application_approvals = Fellowshipapplication.objects.all().order_by('-pk')
        context["fellowship_list"] = self.get_queryset()
        context["fellowship_applications"] = fellowship_applications
        context["application_approvals"] = application_approvals
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
                'active_fellowship': Fellowship.count_all_active()
                }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateFellowshipView(LoginRequiredMixin, CreateView):
    model = Fellowship
    form_class = FellowshipForm
    template_name = "create_fellowship.html"

    def dispatch(self, request, *args, **kwargs):

        self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateFellowshipView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFellowshipView, self).get_form_kwargs()
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
        # Save Fellowship
        fellowshipobject = form.save(commit=False)

        fellowshipobject.created_by = self.request.user

        fellowshipobject.save()
        form.save_m2m()
        if self.request.POST.get("savenewform"):
            return redirect("fellowship:new_account")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'fellowship:list'), 'error': False}
            return JsonResponse(data)

        return redirect("fellowship:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFellowshipView, self).get_context_data(**kwargs)
        context["fellowship_form"] = context["form"]
        context["users"] = self.users
        return context

class FellowshipCommentsView(FormView):
    form_class = FellowshipCommentForm

    def post(self, request, *args, **kwargs):
        gc_form = FellowshipCommentForm(request.POST)
        try:
            gc_form.is_valid()
        except:
            pass
        gc = FellowshipComment(comment=gc_form.cleaned_data['comment'])
        gc.fellowship = Fellowship.objects.get(id=gc_form.cleaned_data.get('fellowship'))
        gc.created_by = User.objects.get(id=gc_form.cleaned_data.get('created_by'))
        gc.save()
        return HttpResponseRedirect(reverse("fellowship:review_fellowship",kwargs={"pk": gc.fellowship.id}))

    def get_success_url(self):
        return reverse("fellowship:review_fellowship",kwargs={"pk": self.fellowship_id})

class FellowshipReviewView(LoginRequiredMixin, DetailView):
    model = Fellowship
    context_object_name = "fellowshiprecord"
    template_name = "review_fellowship.html"

    def get_context_data(self, **kwargs):
        context = super(FellowshipReviewView, self).get_context_data(**kwargs)
        context["fellowship"] = self.object
        context["comments_form"] = FellowshipCommentForm
        fellowshiprecord = context["fellowship"]
        comment_permission = True if (
            self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False
        context['comment_permission'] = comment_permission,
        return context


class FellowshipUpdateView( LoginRequiredMixin, UpdateView):
    model = Fellowship
    form_class = FellowshipForm
    template_name = "create_fellowship.html"

    def get_form_kwargs(self):
        kwargs = super(FellowshipUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Fellowship
        fellowshipobject = form.save(commit=False)
        fellowshipobject.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'fellowship:list'), 'error': False}
            return JsonResponse(data)
        return redirect("fellowship:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FellowshipUpdateView, self).get_context_data(**kwargs)
        context["fellowshipobj"] = self.object

        context["fellowship_form"] = context["form"]
        return context

class FellowshipTypeListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = FellowshipType
    context_object_name = "fellowship_types"
    template_name = "fellowshipType.html"
    current_menu_item = 'fellowships'

    def get_queryset(self):
        queryset = self.model.objects.order_by('-id')

        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    Q(name__icontains=request_post.get('name')))
         
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(FellowshipTypeListView, self).get_context_data(**kwargs)
        context["fellowship_types"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
     
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

# Create Fellowship call
class CreateFellowshipTypeView(LoginRequiredMixin, CreateView,SuccessMessageMixin):
    model = FellowshipType
    form_class = FellowshipTypeForm
    template_name = "create_fellowship_type.html"


    def dispatch(self, request, *args, **kwargs):

        return super(CreateFellowshipTypeView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFellowshipTypeView, self).get_form_kwargs()
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
        # Save Call
        callobject = form.save(commit=False)
        callobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'fellowship:fellowship_type_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Type was created successfully.')
        #messages.success(self.request, 'Call was created successfully!')
        return redirect("fellowship:fellowship_type_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFellowshipTypeView, self).get_context_data(**kwargs)
        context["call_form"] = context["form"]

        return context

#update scholarship call
class FellowshipTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = FellowshipType
    form_class = FellowshipTypeForm
    template_name = "create_fellowship_type.html"

    def dispatch(self, request, *args, **kwargs):

        return super(FellowshipTypeUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FellowshipTypeUpdateView, self).get_form_kwargs()

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Call
        callobject = form.save(commit=False)
        callobject.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'fellowship:fellowship_type_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Type was updated successfully.')
        return redirect("fellowship:fellowship_type_list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FellowshipTypeUpdateView, self).get_context_data(**kwargs)
        context["callobj"] = self.object
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        context["callform"] = context["form"]
        return context

# Fellowship call details
class FellowshipTypeDetailView(LoginRequiredMixin, DetailView):
    model = FellowshipType
    context_object_name = "fellowship_type"
    template_name = "view_fellowship_type.html"

    def get_context_data(self, **kwargs):
        context = super(FellowshipTypeDetailView, self).get_context_data(**kwargs)
        fellowship_type = context["fellowship_type"]

        context.update({

        })
        return context

# Delete fellowship call
class FellowshipTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = FellowshipType
    template_name = 'view_fellowshipcall.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        self.object.delete()
        return redirect("fellowship:fellowship_type_list")
