import datetime
import os

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models import Q
from django.http import (HttpResponseRedirect,
                         JsonResponse, HttpResponse,
                         Http404)
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from calls.models import Call, GrantCall, FellowshipCall
from common.forms import (
    UserForm, LoginForm, UserProfileForm,
    ChangePasswordForm, PasswordResetEmailForm,
    GroupForm, DocumentForm
)
from contacts.models import User, Student
from dashcharts.views.engine import ChartEngine
from events.models import Event
from fellowship.models import Fellowship
from fellowship_applications.models import Fellowshipapplication
from grants.models import Grant
from grants.models import Studentmembership
from grants_applications.models import Grantapplication, Grantappreview
from hrm.models import StaffProfile
from pme.models import Workplan, Activity, Task, TaskReport
from scholarships.models import Scholarshipapplication, Scholarship
from student_reports.models import Studentreport
from .forms import SignUpForm
from .models import Document
from .tokens import account_activation_token
from .utils import has_group


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your RUFORUM Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('common:account_activation_sent')
    # else:
    #     print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        group = Group.objects.get(name='Applicants')
        user.groups.add(group)
        user.save()
        login(request, user)
        return redirect('common:home')
    else:
        return render(request, 'account_activation_invalid.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


class AdminRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        # if not request.user.role == "ADMIN":
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_chart_context(self):
        """construct data form a source and send it to the chart engine"""
        charts = []

        chart_setup = {
            'chart_name': 'testchart',
            'chart_type': 'bar',
            'chart_labels': list(range(2010, 2020)),
            'options': 'options',
            'datasets': {
                'Female': [],
                'Male': []
            }
        }

        for year in range(2010, 2020):
            for gender in ['Female', 'Male']:
                count = Scholarshipapplication.objects.filter(
                    call__start_date__year=year,
                    user__gender=gender.lower()
                ).count()
                chart_setup['datasets'][gender].append(count)

        engine = ChartEngine(**chart_setup)
        chart = engine.make_chart()
        charts.append(chart)

        return charts

    # display charts using django-chartsjs using chart.js

    def get_template_names(self):
        if has_group(self.request.user, 'Students') and has_group(self.request.user, 'Applicants'):
            template_name = 'student_index.html'
        elif has_group(self.request.user, 'Grants Managers'):
            template_name = 'grant_manager_index.html'
        elif has_group(self.request.user, 'Applicants'):
            template_name = 'applicant_index.html'
        elif has_group(self.request.user, 'Students'):
            template_name = 'student_index.html'
        elif has_group(self.request.user, 'Grant Application Reviewers'):
            template_name = 'reviewer_index.html'
        elif has_group(self.request.user, 'Administrative/HR'):
            template_name = 'hr_index.html'
        elif has_group(self.request.user, 'Planning, Monitoring & Evaluation'):
            template_name = 'pme_index.html'
        elif has_group(self.request.user, 'Scholarship Reviewers'):
            template_name = 'sholarship_reviewer.html'
        elif has_group(self.request.user, 'PIs'):
            template_name = 'pi_index.html'
        elif has_group(self.request.user, 'Contacts managers'):
            template_name = 'contacts_manager_index.html'
        elif has_group(self.request.user, 'View & Add Contacts & Events'):
            template_name = 'view_add_contacts_index.html'
        elif has_group(self.request.user, 'Training Team'):
            template_name = 'training_team_index.html'
        elif has_group(self.request.user, 'Scholarship Managers'):
            template_name = 'scholarship_manager_index.html'
        elif has_group(self.request.user, 'Grants Team'):
            template_name = 'grants_team_index.html'
        elif has_group(self.request.user, 'Staffs'):
            template_name = 'staff_index.html'
        elif has_group(self.request.user, 'Project managers'):
            template_name = 'project_managers_index.html'
        else:
            template_name = self.template_name
        return [template_name]

    def get_applicant_context(self):
        context = {}
        context["scholarships_count"] = self.request.user.scholarshipapplication_set.all().count()
        context["grantapplications_count"] = self.request.user.applications.all().count()
        context["fellowshipapplications_count"] = self.request.user.fellowship_applications.all().count()
        context["grants"] = self.request.user.applications.all()
        context["scholarships"] = self.request.user.scholarshipapplication_set.all()
        context['submited_student_reports'] = Studentreport.objects.filter(state='submitted', student=self.request.user)
        context['pending_student_reports'] = Studentreport.objects.filter(state='draft', student=self.request.user)

        return context

    def get_grant_manager_context(self):
        context = {}
        context["calls_count_grants"] = GrantCall.get_grant_calls().count()
        context["calls_count_scholarships"] = Call.get_scholarship_calls().count()
        context["calls_count"] = context["calls_count_grants"] + context["calls_count_scholarships"]
        context['scholarships_count'] = Scholarship.objects.count()
        context['fellowship_count'] = Fellowship.objects.count()
        context["grants_count"] = Grant.objects.all().count()
        context['fellowship_application_count'] = Fellowshipapplication.objects.filter(state='submitted').count()
        context["grant_applications_count"] = Grantapplication.objects.filter(status='submitted').count()
        context['scholarship_applications_count'] = Scholarshipapplication.objects.filter(state='submitted').count()
        return context

    def get_reviewer_context(self):
        context = {}
        context["calls_count_grants"] = GrantCall.get_grant_calls().count()
        context["calls_count_scholarships"] = Call.get_scholarship_calls().count()
        context["calls_count"] = context["calls_count_grants"] + context["calls_count_scholarships"]
        context["grantapplications_count"] = Grantapplication.objects.filter(reviewers=self.request.user,
                                                                             status='validated').exclude(
            reviews__reviewer=self.request.user).distinct().count()
        context["reviewed_grantapplications_count"] = Grantappreview.objects.filter(
            reviewer=self.request.user
        ).count()
        context["scholarshipapplication_count"] = Scholarshipapplication.objects.filter(
            reviewers=self.request.user.pk, reviews__isnull=True,
        ).count()
        context["reviewedscholarshipapplication_count"] = Scholarshipapplication.objects.filter(
            reviews__reviewer=self.request.user.pk, reviews__isnull=False,
        ).count()
        return context

    def get_hr_context(self):
        context = {}
        context['male_staff_count'] = StaffProfile.objects.filter(user__gender='male').count()
        context['female_staff_count'] = StaffProfile.objects.filter(user__gender='female').count()
        context['documents_count'] = Document.objects.all().count()
        context['coming_events_count'] = Event.objects.filter(start_date__gte=datetime.date.today()).count()
        return context

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if has_group(self.request.user, 'Grants Managers'):
            return self.get_grant_manager_context()
        if has_group(self.request.user, 'Applicants') or has_group(self.request.user, 'Students'):
            return self.get_applicant_context()
        if has_group(self.request.user, 'Grant Application Reviewers'):
            return self.get_reviewer_context()
        if has_group(self.request.user, 'Administrative/HR'):
            print("user is HR")
            return self.get_hr_context()
        # scholarship review context
        if has_group(self.request.user, 'Scholarship Reviewers'):
            return self.get_reviewer_context()

        context["contacts_count"] = User.objects.filter(is_active=True).count()
        context["calls_count_grants"] = GrantCall.get_grant_calls().count()
        context["calls_count_scholarships"] = Call.get_scholarship_calls().count()
        context["calls_count"] = context["calls_count_grants"] + context["calls_count_scholarships"]
        context["grants_count"] = Grant.objects.all().count()
        context["student_count"] = Student.objects.all().count()
        context["scholarships_count"] = Scholarshipapplication.objects.all().count()
        context['pi_students'] = Studentmembership.objects.filter(grant__pi=self.request.user).count()
        context['workplan_count'] = Workplan.objects.filter(created_by=self.request.user).count()
        context['activities_count'] = Activity.objects.filter(created_by=self.request.user).count()
        context['task_in_progress'] = Task.objects.filter(
            Q(id__in=TaskReport.objects.filter(status='in_progress').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='failed').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='not_started').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='completed').values_list('task'))).values_list('id')
        context['task_not_started'] = Task.objects.filter(
            Q(id__in=TaskReport.objects.filter(status='not_started' or None).values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='failed').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='in_progress').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='completed').values_list('task'))).values_list('id')
        context['task_completed'] = Task.objects.filter(
            Q(id__in=TaskReport.objects.filter(status='completed').values_list('task')))

        context['task_failed'] = Task.objects.filter(
            Q(id__in=TaskReport.objects.filter(status='failed').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='in_progress').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='not_started').values_list('task'))
            , ~Q(id__in=TaskReport.objects.filter(status='completed').values_list('task'))).values_list('id')
        context["male_contact_count"] = User.objects.filter(gender='male').count()
        context["female_contact_count"] = User.objects.filter(gender='female').count()
        context["grantapplications_validation_count"] = Grantapplication.objects.filter(
            Q(validated_university_letter__isnull=False), validators=self.request.user,
            status='validated',

            ).distinct().count()
        context["grantapplications_to_validate"] = Grantapplication.objects.filter(
            Q(validated_university_letter__isnull=True), validators=self.request.user,
            status='submitted', ).distinct().count()

        return context


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = "change_password.html"

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context["change_password_form"] = ChangePasswordForm()
        return context

    def post(self, request, *args, **kwargs):
        error, errors = "", ""
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            # if not check_password(request.POST.get('CurrentPassword'),
            #                       user.password):
            #     error = "Invalid old password"
            # else:
            user.set_password(request.POST.get('Newpassword'))
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/')
        else:
            errors = form.errors
        return render(request, "change_password.html",
                      {'error': error, 'errors': errors,
                       'change_password_form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["user_obj"] = self.request.user
        return context


class LoginView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():

            user = User.objects.filter(business_email=request.POST.get('business_email')).first()
            # user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    user = authenticate(username=request.POST.get(
                        'business_email'), password=request.POST.get('password'))

                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect('/')
                    return render(request, "login.html", {
                        "error": True,
                        "message":
                            "Your username and password didn't match. \
                            Please try again."
                    })
                return render(request, "login.html", {
                    "error": True,
                    "message":
                        "Your Account is inactive. Please Contact Administrator"
                })
            return render(request, "login.html", {
                "error": True,
                "message":
                    "Your Account is not Found. Please Contact Administrator"
            })
        print(form.errors)
        return render(request, "login.html", {
            "error": True,
            "message": "Your username and password didn't match. Please try again.",
            "form": form
        })


class ForgotPasswordView(TemplateView):
    template_name = "forgot_password.html"


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect("common:login")


class UsersListView(AdminRequiredMixin, TemplateView):
    model = User
    context_object_name = "users"
    template_name = "list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        if request_post:
            if request_post.get('username'):
                queryset = queryset.filter(
                    first_name__icontains=request_post.get('username'))
            if request_post.get('lastname'):
                queryset = queryset.filter(
                    last_name__icontains=request_post.get('lastname'))
            if request_post.get('business_email'):
                queryset = queryset.filter(
                    business_email__icontains=request_post.get('business_email'))
            if request_post.get('group'):
                queryset = queryset.filter(groups=request_post.get('group'))
        group_id = self.request.GET.get('gid')
        if group_id:
            queryset = queryset.filter(groups=group_id).distinct()
        return queryset.order_by('first_name', 'last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        active_users = self.get_queryset().filter(is_active=True)
        inactive_users = self.get_queryset().filter(is_active=False)
        context["active_users"] = active_users
        context["inactive_users"] = inactive_users
        context["per_page"] = self.request.POST.get('per_page')
        # context['admin_email'] = settings.ADMIN_EMAIL
        context['groups'] = Group.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateUserView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data.get("password"):
            user.set_password(form.cleaned_data.get("password"))
        user.save()
        #
        if self.request.POST.getlist('groups'):
            user.groups.add(*self.request.POST.getlist('groups'))
        form.save_m2m()
        # send_email_to_new_user.delay(user.email, self.request.user.email,
        #                             domain=current_site, protocol=protocol)
        # mail_subject = 'Created account in CRM'
        # message = render_to_string('new_user.html', {
        #     'user': user,
        #     'created_by': self.request.user

        # })
        # email = EmailMessage(mail_subject, message, to=[user.email])
        # email.content_subtype = "html"
        # email.send()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:users_list'), 'error': False}
            return JsonResponse(data)

        return super(CreateUserView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CreateUserView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response

    def get_form_kwargs(self):
        kwargs = super(CreateUserView, self).get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context["user_form"] = context["form"]
        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    context_object_name = "users"
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user_obj = self.object
        users_data = []
        for each in User.objects.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.business_email
            users_data.append(assigned_dict)
        context.update({
            "user_obj": user_obj
        })
        return context


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        if self.request.is_ajax():
            if not self.request.user.is_superuser:
                print("user is not superuser")
                # if self.request.user.id != self.object.id:
                data = {'error_403': True, 'error': True}
                return JsonResponse(data)
        # if user.role == "USER":
        #    user.is_superuser = False
        user.save()
        # if self.request.POST.getlist('groups'):
        #  user.groups.add(*self.request.POST.getlist('groups'))

        form.save_m2m()
        if (self.request.user.is_superuser):
            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                    'common:users_list'), 'error': False}
                return JsonResponse(data)
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:users_list'), 'error': False}
            return JsonResponse(data)
        # return redirect("common:users_list")
        return super(UpdateUserView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(UpdateUserView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response

    def get_form_kwargs(self):
        kwargs = super(UpdateUserView, self).get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context["user_obj"] = self.object
        context["user_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "update_profile.html"
    success_url = reverse_lazy("common:home")

    def form_valid(self, form):
        user = form.save(commit=False)

        user.save()
        form.save_m2m()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:profile'), 'error': False}
            return JsonResponse(data)
        return super(UpdateProfileView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(UpdateProfileView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response

    def get_form_kwargs(self):
        kwargs = super(UpdateProfileView, self).get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        context["user_obj"] = self.object
        context["user_form"] = context["form"]

        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_site = request.get_host()
        # send_email_user_delete.delay(
        #    self.object.email, domain=current_site, protocol=request.scheme)
        self.object.delete()
        return redirect("common:users_list")


class PasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetEmailForm
    email_template_name = 'registration/password_reset_email.html'
    from_email = 'nonereply@ruforum.org'


def change_password_by_admin(request):
    if request.user.role == "ADMIN" or request.user.is_superuser:
        if request.method == "POST":
            user = get_object_or_404(User, id=request.POST.get("user_id"))
            # password = User.objects.make_random_password(length=8)
            password = request.POST.get("password")
            print(password)
            user.set_password(password)
            user.save()
            mail_subject = 'Ruforum Account Password Changed'
            message = "<h3><b>hello</b> <i>" + user.first_name + \
                      "</i></h3><br><h2><p> <b>Your account password has been changed !\
                       </b></p></h2>" \
                      + "<br> <p><b> New Password</b> : <b><i>" + \
                      password + "</i><br></p>"
            email = EmailMessage(mail_subject, message, to=[user.business_email], from_email="nonereply@ruforum.org")
            email.content_subtype = "html"
            email.send()
            return HttpResponseRedirect('/users/list/')
    raise PermissionDenied


def change_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
        group = Group.objects.get(name='Applicants')
        user.groups.add(group)
    # user.is_active=True
    user.save()
    current_site = request.get_host()
    # send_email_user_status.delay(
    #  pk, domain=current_site, protocol=request.scheme)'''
    return HttpResponseRedirect('/users/list/')


class GroupsListView(AdminRequiredMixin, TemplateView):
    model = Group
    context_object_name = "groups"
    template_name = "group_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        if request_post:
            if request_post.get('groupname'):
                queryset = queryset.filter(
                    name__icontains=request_post.get('groupname'))
        
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(GroupsListView, self).get_context_data(**kwargs)
        groups = self.get_queryset()
        context["groups"] = groups

        context["per_page"] = self.request.POST.get('per_page')
        # context['admin_email'] = settings.ADMIN_EMAIL
        # context['roles'] = ROLES
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateGroupView(AdminRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "group_create.html"

    def form_valid(self, form):
        group = form.save()
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:groups_list'), 'error': False}
            return JsonResponse(data)
        return super(CreateGroupView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CreateGroupView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response

    def get_form_kwargs(self):
        kwargs = super(CreateGroupView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateGroupView, self).get_context_data(**kwargs)
        context["group_form"] = context["form"]
        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class GroupDetailView(AdminRequiredMixin, DetailView):
    model = Group
    context_object_name = "groups"
    template_name = "group_detail.html"

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        group_obj = self.object
        groups_data = []
        for each in Group.objects.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.name
            groups_data.append(assigned_dict)
        context.update({
            "group_obj": group_obj,
            # "opportunity_list":
            # Opportunity.objects.filter(assigned_to=group_obj.id),
            # "contacts": Contact.objects.filter(assigned_to=group_obj.id),
            # "cases": Case.objects.filter(assigned_to=group_obj.id),
            # "accounts": Account.objects.filter(assigned_to=group_obj.id),
            # "assigned_data": json.dumps(groups_data),
            # "comments": group_obj.group_comments.all(),
        })
        return context


class UpdateGroupView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "group_create.html"

    def form_valid(self, form):
        group = form.save()
        if self.request.is_ajax():
            if (self.request.user.role != "ADMIN" and not
            self.request.user.is_superuser):
                if self.request.user.id != self.object.id:
                    data = {'error_403': True, 'error': True}
                    return JsonResponse(data)

        # if (self.request.user.role == "ADMIN" and
        #        self.request.user.is_superuser):
        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'common:groups_list'), 'error': False}
            return JsonResponse(data)

        return super(UpdateGroupView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(UpdateGroupView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response

    def get_form_kwargs(self):
        kwargs = super(UpdateGroupView, self).get_form_kwargs()
        # kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        context["group_obj"] = self.object
        context['group_form'] = context['form']
        if "errors" in kwargs:
            context["errors"] = kwargs["errors"]
        return context


class GroupDeleteView(AdminRequiredMixin, DeleteView):
    model = Group

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_site = request.get_host()
        # send_email_group_delete.delay(
        #  self.object.email, domain=current_site, protocol=request.scheme)
        self.object.delete()
        return redirect("common:groups_list")


@login_required
def document_create(request):
    template_name = "doc_create.html"
    users = []
    if request.user.role == 'ADMIN' or request.user.is_superuser or has_group(request.user, 'Administrative/HR'):
        users = User.objects.filter(is_active=True, staffprofile__isnull=False).order_by('first_name', 'last_name')
    else:
        users = User.objects.filter(role='ADMIN').order_by('first_name', 'last_name')
    form = DocumentForm(users=users)
    if request.POST:
        form = DocumentForm(request.POST, request.FILES, users=users)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            if request.POST.getlist('shared_to'):
                doc.shared_to.add(*request.POST.getlist('shared_to'))

            data = {'success_url': reverse_lazy(
                'common:doc_list'), 'error': False}
            return JsonResponse(data)
        return JsonResponse({'error': True, 'errors': form.errors})
    context = {}
    context["doc_form"] = form
    context["users"] = users
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist('assigned_to', []) if i]
    context["errors"] = form.errors
    return render(request, template_name, context)


class DocumentListView(LoginRequiredMixin, TemplateView):
    model = Document
    context_object_name = "documents"
    template_name = "doc_list_1.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.user.is_superuser or self.request.user.role == "ADMIN" or has_group(self.request.user,
                                                                                            'Administrative/HR'):
            queryset = queryset
        else:
            if self.request.user.documents():
                doc_ids = self.request.user.documents().values_list('id',
                                                                    flat=True)
                shared_ids = queryset.filter(
                    Q(status='active') &
                    Q(shared_to__id__in=[self.request.user.id])).values_list(
                    'id', flat=True)
                queryset = queryset.filter(
                    Q(id__in=doc_ids) | Q(id__in=shared_ids))
            else:
                queryset = queryset.filter(Q(status='active') & Q(
                    shared_to__id__in=[self.request.user.id]))

        request_post = self.request.POST
        if request_post:
            if request_post.get('doc_name'):
                queryset = queryset.filter(
                    title__icontains=request_post.get('doc_name'))
            if request_post.get('status'):
                queryset = queryset.filter(status=request_post.get('status'))

            if request_post.getlist('shared_to'):
                queryset = queryset.filter(
                    shared_to__id__in=request_post.getlist('shared_to'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(
            groups__name__in=['Administrative/HR', 'Staff'],
            is_active=True).order_by('first_name', 'last_name')
        context["documents"] = self.get_queryset()
        context["status_choices"] = Document.DOCUMENT_STATUS_CHOICE
        context["sharedto_list"] = [
            int(i) for i in self.request.POST.getlist('shared_to', []) if i]
        context["per_page"] = self.request.POST.get('per_page')

        search = False
        if (
                self.request.POST.get('doc_name') or
                self.request.POST.get('status') or
                self.request.POST.get('shared_to')
        ):
            search = True

        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document

    def get(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            if not request.user == Document.objects.get(id=kwargs['pk']).created_by:
                raise PermissionDenied
        self.object = self.get_object()
        self.object.delete()
        return redirect("common:doc_list")


@login_required
def document_update(request, pk):
    template_name = "doc_create.html"
    users = []
    if request.user.role == 'ADMIN' or request.user.is_superuser or has_group(request.user, 'Administrative/HR'):
        users = User.objects.filter(is_active=True, staffprofile__isnull=False).order_by('first_name', 'last_name')
    else:
        users = User.objects.filter(role='ADMIN').order_by('first_name', 'last_name')
    document = Document.objects.filter(id=pk).first()
    form = DocumentForm(users=users, instance=document)

    if request.POST:
        form = DocumentForm(request.POST, request.FILES,
                            instance=document, users=users)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.save()

            doc.shared_to.clear()
            if request.POST.getlist('shared_to'):
                doc.shared_to.add(*request.POST.getlist('shared_to'))

            if request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=request.POST.getlist(
                    'teams')).values_list('users', flat=True)
                assinged_to_users_ids = doc.shared_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        doc.shared_to.add(user_id)

            data = {'success_url': reverse_lazy(
                'common:doc_list'), 'error': False}
            return JsonResponse(data)
        return JsonResponse({'error': True, 'errors': form.errors})
    context = {}
    context["doc_obj"] = document
    context["doc_form"] = form
    context["doc_file_name"] = context["doc_obj"].document_file.name.split(
        "/")[-1]
    context["users"] = users
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist('shared_to', []) if i]
    context["errors"] = form.errors
    return render(request, template_name, context)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "doc_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            if (not request.user ==
                    Document.objects.get(id=kwargs['pk']).created_by):
                raise PermissionDenied

        return super(DocumentDetailView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        # documents = Document.objects.all()
        context.update({
            "file_type_code": self.object.file_type()[1],
            "doc_obj": self.object,
        })
        return context


def download_document(request, pk):
    # doc_obj = Document.objects.filter(id=pk).last()
    doc_obj = Document.objects.get(id=pk)
    if doc_obj:
        if not request.user.role == 'ADMIN':
            if (not request.user == doc_obj.created_by and
                    request.user not in doc_obj.shared_to.all()):
                raise PermissionDenied
        if settings.STORAGE_TYPE == "normal":
            # print('no no no no')
            path = doc_obj.document_file.path
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                                                      os.path.basename(file_path)
                    return response
        else:
            file_path = doc_obj.document_file
            file_name = doc_obj.title
            # print(file_path)
            # print(file_name)
            BUCKET_NAME = "django-crm-demo"
            KEY = str(file_path)
            s3 = boto3.resource('s3')
            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, file_name)
                # print('got it')
                with open(file_name, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                                                      os.path.basename(file_name)
                os.remove(file_name)
                return response
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

            return path
    raise Http404


def download_attachment(request, pk):
    attachment_obj = Attachments.objects.filter(id=pk).last()
    if attachment_obj:
        if settings.STORAGE_TYPE == "normal":
            path = attachment_obj.attachment.path
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                                                      os.path.basename(file_path)
                    return response
        else:
            file_path = attachment_obj.attachment
            file_name = attachment_obj.file_name
            # print(file_path)
            # print(file_name)
            BUCKET_NAME = "django-crm-demo"
            KEY = str(file_path)
            s3 = boto3.resource('s3')
            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, file_name)
                with open(file_name, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + \
                                                      os.path.basename(file_name)
                os.remove(file_name)
                return response
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
            # if file_path:
            #     print('yes tus pus')
    raise Http404


def csrf_failure(request, reason=""):
    ctx = {'message': 'An error has occured !'}
    return render(request, 'csrf_403.html', ctx)


def getUserData(request, *args, **kwargs):
    labels = []
    data = []
    inactive = []

    queryset = Group.objects.filter(user__is_active=True).values('name').annotate(users=Count('user__id')).order_by(
        '-name')
    for entry in queryset:
        labels.append(entry['name'])
        data.append(entry['users'])
    queryset = Group.objects.filter(user__is_active=False).values('name').annotate(
        inactiveusers=Count('user__id')).order_by('-name')
    for entry in queryset:
        inactive.append(entry['inactiveusers'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'inactiveusers': inactive,
    })


def getCallsData(request, *args, **kwargs):
    grantlabels = []
    scholarshiplabels = []
    fellowshiplabels = []
    grants = []
    scholarships = []
    fellowships = []

    queryset = GrantCall.objects.filter(submission_deadline__gte=datetime.date.today()).values('call_id').annotate(
        applications=Count('grantapplication__id')).order_by('grant_type')
    for entry in queryset:
        grantlabels.append(entry['call_id'])
        grants.append(entry['applications'])
    queryset = Call.objects.filter(submission_deadline__gte=datetime.date.today()).values('call_id').annotate(
        scholarship_applications=Count('scholarshipapplication__id')).order_by('scholarship_type')
    for entry in queryset:
        scholarshiplabels.append(entry['call_id'])
        scholarships.append(entry['scholarship_applications'])

    queryset = FellowshipCall.objects.filter(submission_deadline__gte=datetime.date.today()).values('call_id').annotate(
        fellowship_applications=Count('fellowshipapplication__id')).order_by('call_id')
    for entry in queryset:
        fellowshiplabels.append(entry['call_id'])
        fellowships.append(entry['fellowship_applications'])

    return JsonResponse(data={
        'grantlabels': grantlabels,
        'grants': grants,
        'scholarshipapplications': scholarships,
        'scholarshiplabels': scholarshiplabels,
        'fellowshiplabels': fellowshiplabels,
        'fellowships': fellowships,
    })
