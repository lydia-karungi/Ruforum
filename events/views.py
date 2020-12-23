from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)

#from events.forms import EventForm, EventCommentForm, \
#    EventAttachmentForm, EmailForm

from events.models import Event

from contacts.models import User
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage

from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .forms import EventForm
from navutils import MenuMixin
from django.contrib import messages


class EventsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Event
    context_object_name = "events_list"
    template_name = "events.html"
    current_menu_item = 'events'

    def get_queryset(self):
        queryset = self.model.objects.all()
       
        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in = self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('event_name'):
                queryset = queryset.filter(
                    Q(title__icontains=request_post.get('event_name')))
            if request_post.get('start_date'):
                queryset = queryset.filter(
                    Q(start_date__contains=request_post.get('start_date')))
            if request_post.get('end_date'):
                queryset = queryset.filter(
                    Q(end_date__icontains=request_post.get('end_date')))
            if request_post.get('organiser'):
                queryset = queryset.filter(
                    Q(organizer__icontains=request_post.get('organiser')))
            if request_post.get('location'):
                queryset = queryset.filter(
                    Q(host_city__icontains=request_post.get('location')))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(EventsListView, self).get_context_data(**kwargs)
        context["events"] = self.get_queryset().order_by('-end_date')
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


# create event from here
class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "create_event.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateEventView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateEventView, self).get_form_kwargs()
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
        # Save Event
        eventobject = form.save(commit=False)
        
        eventobject.created_by = self.request.user

        eventobject.save()
        form.save_m2m()
        for user in eventobject.participants.all():
            current_site = get_current_site(self.request)
            subject = 'Ruforum Event'
            message = render_to_string('email_template_event.html', {
                'user': user,
                'domain': current_site.domain,
                'event': eventobject
            })
            user.email_user(subject, message)

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'events:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Event Created successfully.')
        return redirect("events:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateEventView, self).get_context_data(**kwargs)
        context["event_form"] = context["form"]
        
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = "eventrecord"
    template_name = "view_events.html"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        eventrecord = context["eventrecord"]
    
        return context


#SalesAccessRequiredMixin, 
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "create_event.html"

    def dispatch(self, request, *args, **kwargs):
        return super(EventUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EventUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Event
        eventobject = form.save(commit=False)
        eventobject.save()
        form.save_m2m()
        
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'events:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Event updated successfully.')
        return redirect("events:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context["eventobj"] = self.object
        context["eventform"] = context["form"]
        return context


#SalesAccessRequiredMixin, 
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'view_event.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("events:list")