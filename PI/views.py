from contacts.models import Student
from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, TemplateView, ListView, DetailView)
from django.views.generic.edit import FormView

from common.choices import COUNTRY_CHOICES
from contacts.forms import StudentForm
from contacts.models import Student
from contacts.models import User
from grants.models import Grant
from grants.models import Studentmembership
from grants_applications.models import Grantapplication
from .forms import StudentEnrollmentForm, ApplicantEnrollmentForm, StudentEnrollForm, ProjectEventForm
# Create your views here.
from .models import ProjectEvent
from grants_reports .models import TempReport
from rest_framework import viewsets
from rest_framework import permissions
from contacts.serializers import UserSerializer
from rest_framework import filters
from contacts.forms import UpdateStudentForm
from django.contrib import messages


class StudentsListView(LoginRequiredMixin, FormView):
    model = Student
    context_object_name = "student_obj_list"
    template_name = "pi_student_list.html"
    form_class = StudentEnrollmentForm

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('country'):
                queryset = queryset.filter(
                    user__country=request_post.get('country'))
            if request_post.get('university_reg_no'):
                queryset = queryset.filter(
                    university_reg_no=request_post.get('university_reg_no'))
        return queryset.distinct()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        context["student_obj_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context['countries'] = COUNTRY_CHOICES
        search = False
        if (
                self.request.POST.get('first_name') or
                self.request.POST.get('last_name') or
                self.request.POST.get('country')
        ):
            search = True
        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


'''this method handles student enrolment, it picks data from the student list view and posts
it to this method for enrollment'''


class CreateEnrollmentView(LoginRequiredMixin, CreateView):
    model = Studentmembership
    form_class = StudentEnrollForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        return super(CreateEnrollmentView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        if (
                request.user.is_superuser or
                request.user.has_perm('PI.change_studentenrollment')
        ):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)

        data = {
            'error': "You don't have permission to enroll student."}
        return JsonResponse(data)

    def form_valid(self, form):
        enrollment = form.save(commit=False)
        enrollment.save()
        return redirect('PI:student_list')

    def form_invalid(self, form):
        context = {}
        return render(self.request, 'student_list.html', context)

    def get_context_data(self, **kwargs):
        context = super(CreateEnrollmentView, self).get_context_data(**kwargs)
        return context


# list of enrolled students '''

class EnrolledStudentsListView(LoginRequiredMixin, TemplateView):
    model = Studentmembership
    context_object_name = "student_obj_list"
    template_name = "enrolled__student_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(grant__pi=self.request.user)
        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    student__user__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    student__user__last_name__icontains=request_post.get('last_name'))
            if request_post.get('country'):
                queryset = queryset.filter(
                    student__user__country=request_post.get('country'))
            if request_post.get('university_reg_no'):
                queryset = queryset.filter(
                    student__university_reg_no=request_post.get('university_reg_no'))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(EnrolledStudentsListView, self).get_context_data(**kwargs)
        context["student_obj_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context['countries'] = COUNTRY_CHOICES
        search = False
        if (
                self.request.POST.get('first_name') or
                self.request.POST.get('last_name') or
                self.request.POST.get('country')
        ):
            search = True
        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# unroll student
class UnRollView(LoginRequiredMixin, DeleteView):
    model = Studentmembership
    template_name = 'enrolled__student_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("PI:enrolled_students")


# pi reports
class PIReportsListView(LoginRequiredMixin, TemplateView):
    
    model = TempReport
    context_object_name = "grants_list"
    template_name = "pi_report_list.html"

    def get_context_data(self, **kwargs):
        context = super(PIReportsListView, self).get_context_data(**kwargs)
        context["reports_list"] = TempReport.objects.filter(pi=self.request.user.id)
        return context


# Events List
class ProjectEventListView(LoginRequiredMixin, TemplateView):
    model = ProjectEvent
    context_object_name = "project_events_list"
    template_name = "project_events_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(organiser=self.request.user)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Grants Managers').exists():
            queryset = self.model.objects.all().order_by('organiser', '-id')
            print(queryset)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ProjectEventListView, self).get_context_data(**kwargs)
        context["events"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ProjectEventDetailView(LoginRequiredMixin, DetailView):
    model = ProjectEvent
    context_object_name = "event_record"
    template_name = "view_project_event.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectEventDetailView, self).get_context_data(**kwargs)
        event_record = context["event_record"]
        return context


# create PI project event
class ProjectEventCreateView(LoginRequiredMixin, CreateView):
    model = ProjectEvent
    form_class = ProjectEventForm
    template_name = "creat_project_events.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ProjectEventCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProjectEventCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        project_object = form.save(commit=False)
        project_object.organiser = self.request.user
        project_object.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'PI:events'), 'error': False}
            return JsonResponse(data)
        return redirect("PI:events")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ProjectEventCreateView, self).get_context_data(**kwargs)
        context["form"] = context["form"]
        return context


# update pi project event
class ProjectEventUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectEvent
    form_class = ProjectEventForm
    template_name = "creat_project_events.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ProjectEventUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProjectEventUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save the report
        event_object = form.save(commit=False)
        event_object.organiser = self.request.user
        event_object.save()
        return redirect("PI:events")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ProjectEventUpdateView, self).get_context_data(**kwargs)
        context["event_obj"] = self.object
        context["form"] = context["form"]
        return context


# delete event
class DeleteProjectEventView(LoginRequiredMixin, DeleteView):
    model = ProjectEvent
    template_name = 'events_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("PI:events")


# applicant lists
# class ContactsListView
class ApplicantListView(LoginRequiredMixin, TemplateView):
    model = User
    context_object_name = "contact_obj_list"
    template_name = "applicants.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(groups=Group.objects.get(name='Applicants'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    last_name__icontains=request_post.get('last_name'))
            if request_post.get('country'):
                queryset = queryset.filter(
                    country=request_post.get('country'))
            if request_post.get('nationality'):
                queryset = queryset.filter(
                    nationality=request_post.get('nationality'))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ApplicantListView, self).get_context_data(**kwargs)
        context["contact_obj_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        # context["users"] = User.objects.filter(
        #    is_active=True).order_by('email')
        context['countries'] = COUNTRY_CHOICES
        # context["country_list"] = [
        #    int(i) for i in self.request.POST.getlist('country', []) if i]
        search = False
        if (
                self.request.POST.get('first_name') or
                self.request.POST.get('last_name') or
                self.request.POST.get('country')
        ):
            search = True
        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreatePIStudentView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "create_pi_student.html"
    success_url = reverse_lazy("PI:student_list")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        self.enrollment_form = ApplicantEnrollmentForm(self.request.user, request.POST)
        if form.is_valid() and self.enrollment_form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form, self.enrollment_form)

    def form_valid(self, form):
        student = form.save(commit=False)
        studentgroup = Group.objects.get(name='Students')
        student.user.groups.clear()
        student.user.groups.add(studentgroup)
        student_id = Student.objects.latest('id')
        id = student_id.id
        student.student_no = 'RU/' + str(date.today().year) + "/" + format(int(id + 1), "06")
        student.save()
        enrollment = self.enrollment_form.save(commit=False)
        enrollment.student = student
        enrollment.pi = self.request.user
        enrollment.save()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'PI:enrolled_students'), 'error': False}
            return JsonResponse(data)
        return redirect('PI:enrolled_students')

    def form_invalid(self, form, enrollment_form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, enrollment_form=self.enrollment_form,
                                  )
        )

    def get_form_kwargs(self):
        kwargs = super(CreatePIStudentView, self).get_form_kwargs()
        # kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_initial(self, *args, **kwargs):
        initial = super(CreatePIStudentView, self).get_initial(**kwargs)
        initial['user'] = User.objects.get(pk=self.kwargs['user_pk'])
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreatePIStudentView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_pk'])
        pi = self.request.user
        context["enrollment_form"] = context.get('enrollment_form') or ApplicantEnrollmentForm(pi)
        user = User.objects.filter(pk=self.kwargs['user_pk'])
        initial = {
            'user': user,

        }
        context["student_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context

    # pi grants


class GrantsListView(LoginRequiredMixin, TemplateView):
    model = Grant
    context_object_name = "grants_list"
    template_name = "grantsList.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(pi=self.request.user)

        request_post = self.request.POST
        if request_post:
            if request_post.get('hide_expired'):
                today = datetime.date.today()
                queryset = queryset.filter(
                    Q(end_date__gte=today, new_end_date__isnull=True) | Q(new_end_date__gte=today,
                                                                          new_end_date__isnull=False))

            if request_post.get('date_range_start'):
                queryset = queryset.filter(
                    start_date__gte=request_post.get('date_range_start'))
            if request_post.get('date_range_end'):
                queryset = queryset.filter(
                    Q(end_date__lte=request_post.get('date_range_end')) | Q(
                        new_end_date__lte=request_post.get('date_range_end')))

            if request_post.get('grant_id'):
                queryset = queryset.filter(
                    grant_id__icontains=request_post.get('grant_id'))
            if request_post.get('title'):
                queryset = queryset.filter(
                    title__contains=request_post.get('title'))
            if request_post.get('call'):
                queryset = queryset.filter(
                    grant_application__call__title__icontains=request_post.get('call'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        call_id = self.request.GET.get('call_id')
        if call_id:
            queryset = queryset.filter(call=call_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(GrantsListView, self).get_context_data(**kwargs)
        grant_applications = Grantapplication.objects.all()
        application_approvals = Grantapplication.objects.all().order_by('-pk')
        context["grants_list"] = self.get_queryset()
        context["grant_applications"] = grant_applications
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
            'active_grants': self.model.objects.filter(pi=self.request.user, approval_status='approved').count()
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class ApplicantsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = User.objects.filter(groups=Group.objects.get(name='Applicants'))
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['business_email', 'first_name','last_name','gender','passport_no',
    'country','nationality','job_title','institution','personal_email','mobile','department']


    # udpdate students
class UpdatePIStudentView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = UpdateStudentForm
    template_name = "edit_pi_student.html"
    success_url = reverse_lazy("PI:enrolled_students")

    def post(self, request, *args, **kwargs):
        self.object =self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        student = form.save(commit=False)

        student.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'contacts:students_list'), 'error': False}
            return JsonResponse(data)
        messages.add_message(self.request, messages.SUCCESS, 'Student was updated successfully.')
        return super(UpdatePIStudentView, self).form_valid(form)


    def form_invalid(self, form):
        response = super(UpdatePIStudentView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        messages.add_message(self.request, messages.ERROR, 'please correct the errors in the form.')
        return response

    def get_form_kwargs(self):
        kwargs = super(UpdatePIStudentView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdatePIStudentView, self).get_context_data(**kwargs)
        context["student_obj"] = self.object
        context["student_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context