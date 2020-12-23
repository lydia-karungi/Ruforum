# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import calendar
import os
import tempfile

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.formsets import formset_factory

from dateutil.rrule import rrule, DAILY, WEEKLY, HOURLY
from dateutil.relativedelta import relativedelta, MO, SU

'''
from .models import (
    MyUser, Department
)

from .forms import (
    MyUserForm, DepartmentForm, UserFilterForm, CustomFormSet
)

from incidents.models import (
    Incident, PreventiveAction, PreventiveActionDetail,
    ActionPlan
)
from incidents.forms import (
    IncidentForm, PreventiveActionForm, ActionPlanForm
)

from incidents.util import get_capa_tracking_number

import xlsxwriter
'''

@login_required
def home(request):
    
    context = {
       
    }

    return render(request, 'index.html', context=context)


