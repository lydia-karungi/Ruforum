import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)

from calls.forms import ScholarshipCallForm,FellowshipCallForm,CommodityfocusForm,ThemeForm,SubthemeForm
#    CallAttachmentForm, EmailForm

from calls.models import Call,GrantCall, Subtheme,Theme,FellowshipCall,Commodityfocus,FellowshipType
from grant_types.models import Granttype
from contacts.models import User
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .forms import CallForm, CallReviewersForm
from navutils import MenuMixin
from common.utils import has_group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django_weasyprint import WeasyTemplateResponseMixin
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import ScholarshipCallSerializer,GrantCallSerializer, FellowshipCallSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters



#class CallsListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
class CallsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = GrantCall
    context_object_name = "calls_list"
    template_name = "calls.html"
    current_menu_item = 'Calls'

    def get_queryset(self):
        queryset = self.model.objects.filter(grant_type__isnull=False)
        if not self.request.user.has_perm('calls.change_call'):
            today = datetime.date.today()
            queryset = queryset.filter(submission_deadline__gte=today)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(CallsListView, self).get_context_data(**kwargs)

        context["calls"] = self.get_queryset().order_by('-submission_deadline')
   
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ScholarshipCallsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Call
    context_object_name = "calls_list"
    template_name = "scholarship_calls.html"
    current_menu_item = 'calls'

    def get_queryset(self):
        queryset = self.model.objects.filter(scholarship_type__isnull=False).order_by('-id')
        if not self.request.user.has_perm('calls.change_call'):
            today = datetime.date.today()
            queryset = queryset.filter(submission_deadline__gte=today).order_by('-id')
     

        request_post = self.request.POST
        if request_post:
            if request_post.get('call_id'):
                queryset = queryset.filter(
                    call_id__icontains=request_post.get('call_id'))
            if request_post.get('title'):
                queryset = queryset.filter(
                    title__contains=request_post.get('title'))
            if request_post.get('type'):
                queryset = queryset.filter(
                    scholarship_type__icontains=request_post.get('type'))
            if request_post.get('submission_deadline'):
                queryset = queryset.filter(submission_deadline__icontains=request_post.get('submission_deadline'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ScholarshipCallsListView, self).get_context_data(**kwargs)
        context["calls"] = self.get_queryset().order_by('-submission_deadline')
   
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



def load_sub_themes(request):
    theme_id = request.GET.get('theme')
    sub_themes = Subtheme.objects.filter(theme_id=theme_id).order_by('name')
    return render(request, 'subtheme_dropdown_list_options.html', {'sub_themes': sub_themes})


class CreateCallView(LoginRequiredMixin, CreateView):
    model = GrantCall
    form_class = CallForm
    template_name = "create_call.html"

    def dispatch(self, request, *args, **kwargs):

        #self.users = User.objects.filter(is_active=True, groups__name='Students').order_by('first_name', 'last_name')
        return super(
            CreateCallView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateCallView, self).get_form_kwargs()

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

        callobject.created_by = self.request.user
        #generating calling Id automatically
        current_year = str(date.today().year)
        # getting last inserted grant call
        last_call = GrantCall.objects.latest('id')
        generated_call_number = 0
        #getting last call year
        last_call_year = last_call.call_year
        last_inserted_generated_number = last_call.generated_number
        if(last_call_year == str(date.today().year)):
            generated_call_number = last_inserted_generated_number + 1
        else:
            generated_call_number=0+1
        # getting the selected grant type
        grand_type_id = form.cleaned_data['grant_type']

        grant_type_object = Granttype.objects.get(id=grand_type_id.id)
        print(grant_type_object)
        grant_type_name=grant_type_object.name
        generated_id="RU/"+current_year+"/"+grant_type_name+"/"+str(format(int(generated_call_number),"04"))
        callobject.call_id=generated_id
        callobject.generated_number = generated_call_number
        callobject.call_year=current_year
        callobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("calls:new_call")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'calls:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant Call was created successfully.')
        return redirect("calls:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateCallView, self).get_context_data(**kwargs)
        context["call_form"] = context["form"]

        return context



#SalesAccessRequiredMixin,
class CallDetailView(LoginRequiredMixin, DetailView):
    model = GrantCall
    context_object_name = "callrecord"
    template_name = "view_call.html"

    def get_context_data(self, **kwargs):
        context = super(CallDetailView, self).get_context_data(**kwargs)
        callrecord = context["callrecord"]

        context.update({

        })
        return context


#SalesAccessRequiredMixin,
class CallUpdateView(LoginRequiredMixin, UpdateView):
    model = GrantCall
    form_class = CallForm
    template_name = "create_call.html"

    def dispatch(self, request, *args, **kwargs):

        return super(CallUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CallUpdateView, self).get_form_kwargs()

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
        #callobject.tags.clear()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'calls:list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Grant Call was updated successfully.')
        return redirect("calls:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CallUpdateView, self).get_context_data(**kwargs)
        context["callobj"] = self.object       
        context["callform"] = context["form"]

        return context


class CallDeleteView(LoginRequiredMixin, DeleteView,SuccessMessageMixin):
    model = GrantCall
    template_name = 'view_call.html'
    success_url = reverse_lazy('serverlist')
    success_message="Deleted sucessfully"

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("calls:list")


# Create Scholarship call
class CreateScholarshipCallView(LoginRequiredMixin, CreateView,SuccessMessageMixin):
    model = Call
    form_class = ScholarshipCallForm
    template_name = "create_scholarship_call.html"


    def dispatch(self, request, *args, **kwargs):

        return super(CreateScholarshipCallView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateScholarshipCallView, self).get_form_kwargs()
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

        callobject.created_by = self.request.user
            #generating call Id automatically
        current_year = str(date.today().year)
        # getting last inserted grant call
        last_call = Call.objects.latest('id')
        generated_call_number = 0
        #getting last call year
        last_call_year = last_call.call_year
        last_inserted_generated_number = last_call.generated_number
        if(last_call_year == str(date.today().year)):
            generated_call_number = last_inserted_generated_number + 1
        else:
            generated_call_number=0+1
        # getting the selected scholarship type
        scholarship_type = form.cleaned_data['scholarship_type']

        #grant_type_object = Granttype.objects.get(id=grand_type_id.id)
        print(scholarship_type)
        generated_id="RU/"+current_year+"/"+scholarship_type+"/"+str(format(int(generated_call_number),"04"))
        callobject.call_id=generated_id
        callobject.generated_number = generated_call_number
        callobject.call_year=current_year

        callobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("calls:new_call")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'calls:scholarship-list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Call was created successfully.')
        #messages.success(self.request, 'Call was created successfully!')
        return redirect("calls:scholarship-list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateScholarshipCallView, self).get_context_data(**kwargs)
        context["call_form"] = context["form"]

        return context

#update scholarship call
class ScholarshipCallUpdateView(LoginRequiredMixin, UpdateView):
    model = Call
    form_class = ScholarshipCallForm
    template_name = "create_scholarship_call.html"

    def dispatch(self, request, *args, **kwargs):

        return super(ScholarshipCallUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ScholarshipCallUpdateView, self).get_form_kwargs()

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
        #callobject.tags.clear()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'calls:scholarship-list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Scholarship Call was updated successfully.')
        return redirect("calls:scholarship-list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ScholarshipCallUpdateView, self).get_context_data(**kwargs)
        context["callobj"] = self.object
        context["callform"] = context["form"]
        return context

# scholarship call details
class ScholarshipCallDetailView(LoginRequiredMixin, DetailView):
    model = Call
    context_object_name = "callrecord"
    template_name = "view_scholarshipcall.html"

    def get_context_data(self, **kwargs):
        context = super(ScholarshipCallDetailView, self).get_context_data(**kwargs)
        callrecord = context["callrecord"]

        context.update({

        })
        return context

# Delete scholarship call
class ScholarshipCallDeleteView(LoginRequiredMixin, DeleteView):
    model = Call
    template_name = 'view_scholarshipcall.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("calls:scholarship-list")

class FellowshipCallListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = FellowshipCall
    context_object_name = "calls_list"
    template_name = "fellowshipcalls.html"
    current_menu_item = 'calls'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset.distinct()


    def get_context_data(self, **kwargs):
        context = super(FellowshipCallListView, self).get_context_data(**kwargs)

        context["calls"] = self.get_queryset().order_by('-submission_deadline')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# Create Fellowship call
class CreateFellowshipCallView(LoginRequiredMixin, CreateView,SuccessMessageMixin):
    model = FellowshipCall
    form_class = FellowshipCallForm
    template_name = "create_fellowship_call.html"


    def dispatch(self, request, *args, **kwargs):

        return super(CreateFellowshipCallView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFellowshipCallView, self).get_form_kwargs()
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
        #generating calling Id automatically
        current_year = str(date.today().year)
        # getting last inserted grant call
        last_call = FellowshipCall.objects.latest('id')
        generated_call_number = 0
        #getting last call year
        last_call_year = last_call.call_year
        last_inserted_generated_number = last_call.generated_number
        if(last_call_year == str(date.today().year)):
            generated_call_number = last_inserted_generated_number + 1
        else:
            generated_call_number=0+1
        # getting the selected grant type
        fellowship_type_id = form.cleaned_data['fellowship_type']

        fellowship_type_object = FellowshipType.objects.get(id=fellowship_type_id.id)
        print(fellowship_type_object)
        fellowship_type_name=fellowship_type_object.name
        generated_id="RU/"+current_year+"/"+fellowship_type_name+"/"+str(format(int(generated_call_number),"04"))
        callobject.call_id=generated_id
        callobject.generated_number = generated_call_number
        callobject.call_year=current_year
        callobject.save()

        if self.request.POST.get("savenewform"):
            return redirect("calls:new_call")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'calls:fellowship-list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Call was created successfully.')
        #messages.success(self.request, 'Call was created successfully!')
        return redirect("calls:fellowship-list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateFellowshipCallView, self).get_context_data(**kwargs)
        context["call_form"] = context["form"]

        return context

#update scholarship call
class FellowshipCallUpdateView(LoginRequiredMixin, UpdateView):
    model = FellowshipCall
    form_class = FellowshipCallForm
    template_name = "create_fellowship_call.html"

    def dispatch(self, request, *args, **kwargs):

        return super(FellowshipCallUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(FellowshipCallUpdateView, self).get_form_kwargs()

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
                'calls:fellowship-list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Fellowship Call was updated successfully.')
        return redirect("calls:fellowship-list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(FellowshipCallUpdateView, self).get_context_data(**kwargs)
        context["callobj"] = self.object
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        context["callform"] = context["form"]
        return context

# Fellowship call details
class FellowshipCallDetailView(LoginRequiredMixin, DetailView):
    model = FellowshipCall
    context_object_name = "callrecord"
    template_name = "view_fellowshipcall.html"

    def get_context_data(self, **kwargs):
        context = super(FellowshipCallDetailView, self).get_context_data(**kwargs)
        callrecord = context["callrecord"]

        context.update({

        })
        return context

# Delete fellowship call
class FellowshipCallDeleteView(LoginRequiredMixin, DeleteView):
    model = FellowshipCall
    template_name = 'view_fellowshipcall.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        self.object.delete()
        return redirect("calls:scholarship-list")

#print Fellowship call details
class FellowshipCallPrintView(LoginRequiredMixin, DetailView,WeasyTemplateResponseMixin):
    model = FellowshipCall
    context_object_name = "callrecord"
    template_name = "print_fellowshipcall.html"
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # suggested filename (is required for attachment!)
    pdf_filename = 'fellowship_Call.pdf'

#print Grant call details
class GrantCallPrintView(LoginRequiredMixin, DetailView,WeasyTemplateResponseMixin):
    model = GrantCall
    context_object_name = "callrecord"
    template_name = "print_grantcall.html"
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # suggested filename (is required for attachment!)
    pdf_filename = 'grant_Call.pdf'


#print Fellowship call details
class ScholarshipCallPrintView(LoginRequiredMixin, DetailView,WeasyTemplateResponseMixin):
    model = Call
    context_object_name = "callrecord"
    template_name = "print_scholarshipcall.html"
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # suggested filename (is required for attachment!)
    pdf_filename = 'scholarship_Call.pdf'

def CommodityCreatePopup(request):
	form = CommodityfocusForm(request.POST or None)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_author". This is the element id in the form

		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_commodity");</script>' % (instance.pk, instance))

	return render(request, "commodity_form.html", {"form" : form})

def CommodityEditPopup(request, pk = None):
	instance = get_object_or_404(Commodityfocus, pk = pk)
	form = CommodityfocusForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_author". This is the element id in the form

		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_commodity");</script>' % (instance.pk, instance))

	return render(request, "commodity_form.html", {"form" : form})

@csrf_exempt
def get_commodity_id(request):
	if request.is_ajax():
		name = request.GET['name']
		commodity_id = Commodityfocus.objects.get(name = name).id
		data = {'commodity_id':commodity_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")
# theme views
def ThemeCreatePopup(request):
	form = ThemeForm(request.POST or None)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_theme". This is the element id in the form

		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_theme");</script>' % (instance.pk, instance))

	return render(request, "theme_form.html", {"form" : form})

def ThemeEditPopup(request, pk = None):
	instance = get_object_or_404(Theme, pk = pk)
	form = ThemeForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_author". This is the element id in the form

		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_theme");</script>' % (instance.pk, instance))

	return render(request, "theme_form.html", {"form" : form})

@csrf_exempt
def get_theme_id(request):
	if request.is_ajax():
		name = request.GET['name']
		theme_id = Theme.objects.get(name = name).id
		data = {'theme_id':theme_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

# Subtheme views
def SubThemeCreatePopup(request):
	form = SubthemeForm(request.POST or None)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_subtheme". This is the element id in the form

		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_subtheme");</script>' % (instance.pk, instance))

	return render(request, "subtheme_form.html", {"form" : form})

def SubThemeEditPopup(request, pk = None):
	instance = get_object_or_404(Subtheme, pk = pk)
	form = SubthemeForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_subthem". This is the element id in the form

		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_subtheme");</script>' % (instance.pk, instance))

	return render(request, "subtheme_form.html", {"form" : form})

@csrf_exempt
def get_subtheme_id(request):
	if request.is_ajax():
		name = request.GET['name']
		subtheme_id = Subtheme.objects.get(name = name).id
		data = {'subtheme_id':subtheme_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

class CommodityFocusDeleteView(LoginRequiredMixin, DeleteView):
    model = Commodityfocus
    template_name = 'create_call.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        self.object.delete()

        return JsonResponse({'message':'commidity focus deleted successfully!.'})

class ProposalThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = 'create_call.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        self.object.delete()

        return JsonResponse({'message':'theme deleted successfully!.'})

class SubthemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Subtheme
    template_name = 'create_call.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            raise PermissionDenied
        self.object.delete()

        return JsonResponse({'message':'subtheme deleted successfully!.'})


class ScholarshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows calls to be viewed or edited.
    """
    
    serializer_class = ScholarshipCallSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title', 'call_id','submission_deadline','text','start_date',
    'end_date','scholarship_type']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = Call.objects.all().order_by('-id','-submission_deadline')
        if not self.request.user.has_perm('calls.change_call'):
            today = datetime.date.today()
            queryset = queryset.filter(submission_deadline__gte=today).order_by('-id')
        
        return queryset.distinct()
     

class GrantCallViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows calls to be viewed or edited.
    """
    serializer_class = GrantCallSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title', 'call_id','submission_deadline','minimum_qualification','start_date',
    'end_date','grant_type__name','proposal_sub_theme__name','proposal_theme__name','commodity_focus__name']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = GrantCall.objects.filter(grant_type__isnull=False)
        if not self.request.user.has_perm('calls.change_call'):
            today = datetime.date.today()
            queryset = queryset.filter(submission_deadline__gte=today)
        
        return queryset.distinct()


class FellowshipCallViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows calls to be viewed or edited.
    """
    
    serializer_class = FellowshipCallSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['id','title','call_id', 'submission_deadline', 'start_date', 'end_date',
         'duration', 'member_university','home_institute_obligations','host_institute','goal',
         'objectives','who_can_apply','financial_support','institute_obligations','fellowship_type__name']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = FellowshipCall.objects.all().order_by('-id','-submission_deadline')
        if not self.request.user.has_perm('calls.change_call'):
            today = datetime.date.today()
            queryset = queryset.filter(submission_deadline__gte=today)
        
        return queryset.distinct()