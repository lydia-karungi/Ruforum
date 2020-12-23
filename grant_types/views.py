from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)

#from grant_types.forms import GranttypeForm, GranttypeCommentForm, \
#    GranttypeAttachmentForm, EmailForm

from grant_types.models import Granttype #, Tags, Email

from contacts.models import User


from django.urls import reverse_lazy, reverse

#from leads.models import Lead

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required

#from grant_types.tasks import send_email
#from common.tasks import send_email_user_mentions

from django.contrib.sites.shortcuts import get_current_site

from .forms import GranttypeForm

'''
from common.access_decorators_mixins import (
    sales_access_required, marketing_access_required, SalesAccessRequiredMixin, MarketingAccessRequiredMixin)
from teams.models import Teams
'''

#class GranttypesListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
class GranttypesListView(LoginRequiredMixin, TemplateView):
    model = Granttype
    context_object_name = "grant_types_list"
    template_name = "grant_types.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        '''
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            queryset = queryset.filter(created_by=self.request.user.id)
        '''
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in = self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains=request_post.get('name'))
            if request_post.get('city'):
                queryset = queryset.filter(
                    billing_city__contains=request_post.get('city'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GranttypesListView, self).get_context_data(**kwargs)

        #open_grant_types = self.get_queryset().filter(status='open')
        #close_grant_types = self.get_queryset().filter(status='close')
        context["grant_types"] = self.get_queryset()

        context["per_page"] = self.request.POST.get('per_page')
        #tag_ids = list(set(Granttype.objects.values_list('tags', flat=True)))
        #context["tags"] = Tags.objects.filter(id__in=tag_ids)
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


#class CreateGranttypeView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
class CreateGranttypeView(LoginRequiredMixin, CreateView):
    model = Granttype
    form_class = GranttypeForm
    template_name = "create_grant_type.html"

    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateGranttypeView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateGranttypeView, self).get_form_kwargs()
        #kwargs.update({"account": True})
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
        # Save Granttype
        grant_typeobject = form.save(commit=False)

        grant_typeobject.created_by = self.request.user

        grant_typeobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("grant_types:new_account")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grant_types:list'), 'error': False}
            return JsonResponse(data)

        return redirect("grant_types:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateGranttypeView, self).get_context_data(**kwargs)
        context["grant_type_form"] = context["form"]

        return context


class GrantTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Granttype
    form_class = GranttypeForm
    template_name = "create_grant_type.html"

    def dispatch(self, request, *args, **kwargs):

        return super(GrantTypeUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GrantTypeUpdateView, self).get_form_kwargs()

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Call
        grant_type_object = form.save(commit=False)
        grant_type_object.save()
        #callobject.tags.clear()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'grant_types:list'), 'error': False}
            return JsonResponse(data)
        return redirect("grant_types:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(GrantTypeUpdateView, self).get_context_data(**kwargs)
        context["granttypeobj"] = self.object
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        context["grant_type_form"] = context["form"]
        return context
# grant type details
class GrantTypeDetailView(LoginRequiredMixin, DetailView):
    model = Granttype
    context_object_name = "grant_type_record"
    template_name = "view_grant_type.html"

    def get_context_data(self, **kwargs):
        context = super(GrantTypeDetailView, self).get_context_data(**kwargs)
        grant_type_record = context["grant_type_record"]

        context.update({

        })
        return context

class GrantTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = Granttype
    template_name = 'grant_types.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        self.object.delete()
        return redirect('grant_types:list')
