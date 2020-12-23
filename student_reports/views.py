import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, FormView)

from grant_types.models import Granttype
from student_reports.models import Studentreport, Milestone
from contacts.models import User, Student
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .forms import (
    StudentreportForm, ProfileForm, StudentForm, OtherstudentreportForm,SupervisorDetailsForm,
    SkillsImprovementForm,ProductsForm,AdditionInformationForm,ResearchInformationForm,MilestoneFormSet, 
    PublicationFormSet, BriefFormSet, ManuscriptFormSet
)
from navutils import MenuMixin


class MyStudentreportsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Studentreport
    context_object_name = "student_reports_list"
    template_name = "my_student_reports.html"
    current_menu_item = 'my_student_reports'

    def get_context_data(self, **kwargs):
        context = super(MyStudentreportsListView, self).get_context_data(**kwargs)

        periods = Studentreport.PERIOD_CHOICES[:5]
        report_data = []
        for period in periods:
            try:
                report = Studentreport.objects.filter(
                    student=self.request.user,
                    period=period[0]
                )
            except Studentreport.DoesNotExist:
                report = None
            data = {
                'period': period[0],
                'description': period[1],
                'report': report
            }
            report_data.append(data)
        print(report_data)
        context['report_data'] = report_data

        return context


class StudentreportsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Studentreport
    context_object_name = "student_reports_list"
    template_name = "student_reports.html"
    current_menu_item = 'student_reports'

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
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    student__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    student__last_name__icontains=request_post.get('last_name'))
            if request_post.get('type'):
                queryset = queryset.filter(
                    student__grant_type__icontains=request_post.get('type'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(StudentreportsListView, self).get_context_data(**kwargs)
        context["student_reports"] = self.get_queryset().order_by('-submitted_on')
        context["grant_types"] = Granttype.objects.all()
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


class CreateStudentreportView(LoginRequiredMixin, CreateView):
    model = Studentreport
    form_class = StudentreportForm
    template_name = "create_student_report.html"

    def dispatch(self, request, *args, **kwargs):
        return super(CreateStudentreportView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateStudentreportView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.profile_form = ProfileForm(request.POST, request.FILES, instance=self.request.user)
        try:
            student_instance = self.request.user.student
        except Student.DoesNotExist:
            student_instance = None
        self.student_form = StudentForm(request.POST, request.FILES, instance=student_instance)
        self.supervisor_form = SupervisorDetailsForm(request.POST, request.FILES)
        self.researchinformation_form = ResearchInformationForm(request.POST, request.FILES)
        self.skillsimprovement_form = SkillsImprovementForm(request.POST, request.FILES)
        self.products_form = ProductsForm(request.POST, request.FILES)
        self.additioninformation_form = AdditionInformationForm(request.POST, request.FILES)
        self.other_form = OtherstudentreportForm(request.POST, request.FILES)
        self.milestones = MilestoneFormSet(request.POST, request.FILES, prefix='milestone_formset')
        self.publications = PublicationFormSet(request.POST, request.FILES, prefix='publication_formset')
        self.briefs = BriefFormSet(request.POST, request.FILES, prefix='brief_formset')
        self.manuscripts = ManuscriptFormSet(request.POST, request.FILES, prefix='manuscript_formset')

        formsets_valid = (
            self.milestones.is_valid() and self.publications.is_valid() and self.briefs.is_valid() and
            self.manuscripts.is_valid()
        )
        forms_valid = (
            form.is_valid() and self.profile_form.is_valid() and self.student_form.is_valid() and
            self.other_form.is_valid()
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.profile_form.errors)
            print(self.student_form.errors)
            print(self.researchinformation_form.errors)
            print(self.supervisor_form.errors)
            print(self.skillsimprovement_form.errors)
            print(self.products_form.errors)
            print(self.additioninformation_form.errors)
            print(self.other_form.errors)
            print(self.milestones.errors)
            print(self.publications.errors)
            print(self.briefs.errors)
            print(self.manuscripts.errors)
            print("----------------")
        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        student_reportobject = form.save(commit=False)
        student_reportobject.student = self.request.user
        student_reportobject.period = self.kwargs['period']
        student_reportobject.submitted_on = datetime.date.today()
        student_reportobject.save()
        profile = self.profile_form.save()
        profile.is_active = True
        profile.save()
        student = self.student_form.save(commit=False)
        student.user = self.request.user
        student.save()
        other = self.other_form.save(commit=False)
        other.studentreport_ptr = student_reportobject
        other.save()

        self.milestones.instance = student_reportobject
        instances = self.milestones.save(commit=False)
        for i, milestone in enumerate(instances):
            milestone.milestone_type = Milestone.MILESTONE_TYPES[i][0]
            milestone.save()

        self.publications.instance = student_reportobject
        instances = self.publications.save(commit=False)

        self.briefs.instance = student_reportobject
        instances = self.briefs.save(commit=False)

        self.manuscripts.instance = student_reportobject
        instances = self.manuscripts.save(commit=False)

        '''
        if self.request.POST.get("savenewform"):
            return redirect("student_reports:new_student_report")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'student_reports:list'), 'error': False}
            return JsonResponse(data)
        '''
        return redirect("student_reports:my_reports")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=self.profile_form,
                student_form=self.student_form, other_form=self.other_form,
                milestones=self.milestones, publications=self.publications,
                briefs=self.briefs, manuscripts=self.manuscripts)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateStudentreportView, self).get_context_data(**kwargs)
        context["student_report_form"] = context["form"]
        context["profile_form"] = context.get('profile_form') or ProfileForm(instance=self.request.user)
        try:
            student_instance = self.request.user.student
        except Student.DoesNotExist:
            student_instance = None
        context["student_form"] = context.get('student_form') or StudentForm(instance=student_instance)
        context["supervisor_form"] = context.get('supervisor_form') or SupervisorDetailsForm()
        context["researchinformation_form"] = context.get('researchinformation_form') or ResearchInformationForm()
        context["skillsimprovement_form"] = context.get('skillsimprovement_form') or SkillsImprovementForm()
        context["products_form"] = context.get('products_form') or ProductsForm()
        context["additioninformation_form"] = context.get('additioninformation_form') or AdditionInformationForm()
        context["other_form"] = context.get('other_form') or OtherstudentreportForm()
        context["milestone_formset"] = context.get('milestone_formset') or MilestoneFormSet(prefix='milestone_formset')
        context['milestone_types'] = [row[1] for row in Milestone.MILESTONE_TYPES]
        context["publication_formset"] = context.get('publication_formset') or PublicationFormSet(prefix='publication_formset')
        context["brief_formset"] = context.get('brief_formset') or BriefFormSet(prefix='brief_formset')
        context["manuscript_formset"] = context.get('manuscript_formset') or ManuscriptFormSet(prefix='manuscript_formset')
        return context


class StudentreportDetailView(LoginRequiredMixin, DetailView):
    model = Studentreport
    context_object_name = "student_reportrecord"
    template_name = "view_student_report.html"

    def get_context_data(self, **kwargs):
        context = super(StudentreportDetailView, self).get_context_data(**kwargs)
        student_reportrecord = context["student_reportrecord"]
        return context


# update student's report
class StudentreportUpdateView(LoginRequiredMixin, UpdateView):
    model = Studentreport
    form_class = StudentreportForm
    template_name = "create_student_report.html"

    def dispatch(self, request, *args, **kwargs):
        return super(StudentreportUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(StudentreportUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.profile_form = ProfileForm(request.POST, request.FILES, instance=self.request.user)
        try:
            student_instance = self.request.user.student
        except Student.DoesNotExist:
            student_instance = None
        self.student_form = StudentForm(request.POST, request.FILES, instance=student_instance)
        self.other_form = OtherstudentreportForm(request.POST, request.FILES)
        self.milestones = MilestoneFormSet(request.POST, request.FILES, prefix='milestone_formset')
        self.publications = PublicationFormSet(request.POST, request.FILES, prefix='publication_formset')
        self.briefs = BriefFormSet(request.POST, request.FILES, prefix='brief_formset')
        self.manuscripts = ManuscriptFormSet(request.POST, request.FILES, prefix='manuscript_formset')

        formsets_valid = (
            self.milestones.is_valid() and self.publications.is_valid() and self.briefs.is_valid() and
            self.manuscripts.is_valid()
        )
        forms_valid = (
            form.is_valid() and self.profile_form.is_valid() and self.student_form.is_valid() and
            self.other_form.is_valid()
        )
        if forms_valid and formsets_valid:
            return self.form_valid(form)
        else:
            print("invalid!!!!")
            print(form.errors)
            print(self.profile_form.errors)
            print(self.student_form.errors)
            print(self.other_form.errors)
            print(self.milestones.errors)
            print(self.publications.errors)
            print(self.briefs.errors)
            print(self.manuscripts.errors)
            print("----------------")

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Studentreport
        student_reportobject = form.save(commit=False)
        student_reportobject.student = self.request.user
        student_reportobject.period = self.object.period
        student_reportobject.submitted_on = datetime.date.today()
        student_reportobject.save()
        profile = self.profile_form.save()
        profile.is_active = True
        profile.save()
        student = self.student_form.save(commit=False)
        student.user = self.request.user
        student.save()
        other = self.other_form.save(commit=False)
        other.studentreport_ptr = student_reportobject
        other.save()

        self.milestones.instance = student_reportobject
        instances = self.milestones.save(commit=False)
        for i, milestone in enumerate(instances):
            milestone.milestone_type = Milestone.MILESTONE_TYPES[i][0]
            milestone.save()

        self.publications.instance = student_reportobject
        instances = self.publications.save(commit=False)

        self.briefs.instance = student_reportobject
        instances = self.briefs.save(commit=False)

        self.manuscripts.instance = student_reportobject
        instances = self.manuscripts.save(commit=False)

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'student_reports:list'), 'error': False}
            return JsonResponse(data)
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            return redirect("student_reports:my_student_reports")
        return redirect("student_reports:list")

       
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=self.profile_form,
                student_form=self.student_form, other_form=self.other_form,
                milestones=self.milestones, publications=self.publications,
                briefs=self.briefs, manuscripts=self.manuscripts)
        )

    def get_context_data(self, **kwargs):
        context = super(StudentreportUpdateView, self).get_context_data(**kwargs)
        context["student_reportobj"] = self.object
        context["student_report_form"] = context["form"]
        context["profile_form"] = context.get('profile_form') or ProfileForm(instance=self.request.user)
        try:
            student_instance = self.request.user.student
        except Student.DoesNotExist:
            student_instance = None
        context["student_form"] = context.get('student_form') or StudentForm(instance=student_instance)
        context["other_form"] = context.get('other_form') or OtherstudentreportForm()
        context["milestone_formset"] = context.get('milestone_formset') or MilestoneFormSet(prefix='milestone_formset')
        context['milestone_types'] = [row[1] for row in Milestone.MILESTONE_TYPES]
        context["publication_formset"] = context.get('publication_formset') or PublicationFormSet(prefix='publication_formset')
        context["brief_formset"] = context.get('brief_formset') or BriefFormSet(prefix='brief_formset')
        context["manuscript_formset"] = context.get('manuscript_formset') or ManuscriptFormSet(prefix='manuscript_formset')
        return context


class StudentreportDeleteView(LoginRequiredMixin, DeleteView):
    model = Studentreport
    template_name = 'view_student_report.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("student_reports:list")


class SingleStudentreportsListView(MenuMixin, LoginRequiredMixin, TemplateView):
    model = Studentreport
    context_object_name = "student_reports_list"
    template_name = "student_reports.html"
    current_menu_item = 'student_reports'

    def get_queryset(self):
        queryset = self.model.objects.filter(student=self.request.user)

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    student__first_name__icontains=request_post.get('first_name'))
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    student__last_name__icontains=request_post.get('last_name'))
            if request_post.get('type'):
                queryset = queryset.filter(
                    student__grant_type__icontains=request_post.get('type'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(SingleStudentreportsListView, self).get_context_data(**kwargs)
        context["student_reports"] = self.get_queryset().order_by('-submitted_on')
        context["grant_types"] = Granttype.objects.all()


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
