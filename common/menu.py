from navutils import menu

from .utils import has_group

main_menu = menu.Menu('main')
menu.register(main_menu)
schp_reviewer_menu = menu.Menu("scholarship_reviewer")
menu.register(schp_reviewer_menu)
hr_menu = menu.Menu('hr')
menu.register(hr_menu)
project_management_menu = menu.Menu('project_management')
menu.register(project_management_menu)


def can_view_contacts(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('contacts.view_user') or has_group(user, 'Contacts managers') or has_group(user,
                                                                                                    'View & Add Contacts & Events')
def can_manage_projects(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('project_management.view_projectmanagement') or has_group(user, 'Project managers') or has_group(user,
                                                                                                    'manage projects')


def can_view_applicants(user, context):
    if has_group(user, 'PIs'):
        return True


def can_view_students(user, context):
    if user.is_superuser:
        return True
    if has_group(user, 'Admin'):
        return True
    return user.has_perm('contacts.change_student')


def can_view_calls(user, context):
    if user.is_superuser:
        return True
    if has_group(user, 'Students') or has_group(user, 'Applicants') or has_group(user, 'PIs') or has_group(user,
                                                                                                           'Grants Managers') or user.has_perm(
            'calls.view_call'):
        return True
    print("change call", user.has_perm('calls.change_call'))
    return user.has_perm('calls.change_call')
    # can view grant calls


def can_view_grant_calls(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('calls.view_grantcall')

def can_view_leave_applications(user, context):
    return user.has_perm('hrm.view_leaveapplication')

# user can view scholarship calls
def can_view_scholarship_calls(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('calls.view_call')


# user can view fellowship calls
def can_view_fellowship_calls(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('calls.view_fellowshipcall')


# Can view scholarship
def can_view_scholarships(user, context):
    if user.is_superuser:
        return True
    if has_group(user, 'Students') or has_group(user, 'Applicants') or has_group(user, 'Grants Managers') or has_group(
            user, 'Scholarship Reviewers') or user.has_perm('scholarships.view_all'):
        return True

def can_view_leave(user, context):

    if has_group(user, 'Staffs') or has_group(user, 'Administrative/HR'):
        return True

def can_view_appraisals(user, context):
    if has_group(user, 'Staffs') or has_group(user, 'Administrative/HR'):
        return True


def can_manage_users(user, context):
    return user.is_superuser


def can_manage_settings(user, context):
    return user.is_superuser


def can_manage_events(user, context):
    if user.is_superuser:
        return True
    print("change event", user.has_perm('events.change_event'))
    return user.has_perm('events.change_event')


# can view scholarship applications
def can_manage_scholarships(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('scholarships.view_scholarshipapplication')


def can_view_grant_reports(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('PI.view_grantreport') or has_group(user, 'Grants Managers')


def can_view_grant_applications(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('grants_applications.view_grantapplication')


def can_change_student_enrollment(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('PI.change_studentenrollment')


def can_submit_pi_report(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('pireport.change_pireport')


def can_manage_student_reports(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('student_reports.change_studentreport')


def can_validate_applications(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('contacts.can_validate_grant_application')

def can_validate_fellowship_applications(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('contacts.can_validate_grant_application')


def can_review_applications(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('grants_applications.review_grant_applications')


def can_review_scholarships(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('scholarships.mark_scholarship_applications')


def can_make_scholarships_decisions(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('scholarships.change_scholarship')


def can_manage_grants(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('grants.change_grant') or has_group(user, 'Grants Managers')


def can_make_grants_applications_decision(user, context):
    if user.is_superuser:
        return True
    return has_group(user, 'Grants Managers')


def can_view_grants(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('grants.view_grant') or has_group(user, 'Students') or has_group(user,
                                                                                          'Grants Managers') or has_group(
        user, "PIs") or has_group(user, "Grants Team")


def can_manage_fellowship(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('grant.can_change_grant') or has_group(user, 'Grants Managers')


def can_view_fellowship(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('fellowship_applications.view_fellowshipapplication') or has_group(user, 'Staff') or has_group(
        user, 'Grants Managers')


def is_applicant(user, context):
    return has_group(user, 'Applicants')


def is_grant_team_member(user, context):
    return has_group(user, 'Grants Team')


def is_pmeuser(user, context):
    return has_group(user, 'Planning, Monitoring & Evaluation')


def is_hr_manager(user, context):
    return has_group(user, 'Administrative/HR')

def is_project_manager(user, context):
    return has_group(user, 'Project managers')



def is_view_and_add_contacts_manager(user, context):
    return has_group(user, 'View & Add Contacts & Events') or has_group(user, 'Contacts managers')


def is_student(user, context):
    return has_group(user, 'Students')


def can_change_student_report(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('studentreport.can_add_student_report') or has_group(user, 'Students')


def can_change_scholarship_application(user, context):
    return user.has_perm('scholarshipapplication.change_scholarshipapplication') or has_group(user,
                                                                                              'Students') or user.has_perm(
        'scholarshipapplication.can_view_scholarship_application') or has_group(user, 'Applicants') or has_group(user,
                                                                                                                 'Grants Managers')


def can_change_grant_application(user, context):
    return user.has_perm('grantapplication.can_change_grant_application')


menus = [
    menu.Node(id='dashboard', label='Dashboard', pattern_name='common:home', link_attrs={'id': 'dashboard'}),
    menu.PassTestNode(id='contacts', label='Contacts', pattern_name='contacts:list', link_attrs={'id': 'contacts'},
                      test=can_view_contacts),
    menu.PassTestNode(id='students', label='Students', pattern_name='contacts:students_list',
                      link_attrs={'id': 'students'}, test=can_view_students, css_class="active"),
    menu.PassTestNode(
        id='calls-section',
        css_class="calls_class",
        label='Calls',
        url='#',
        test=can_view_calls,
        template='navutils/dropdown.html',
        children=[
            menu.PassTestNode(id='grant_types',
                              label='Grant Types',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='grant_types:list', test=can_manage_grants),
            menu.PassTestNode(id='grant_calls', label='Grant Calls', pattern_name='calls:list',
                              link_attrs={'id': 'calls'}, test=can_view_grant_calls),
            menu.PassTestNode(id='scholarship_calls', label='Scholarship Calls', pattern_name='calls:scholarship-list',
                              link_attrs={'id': 'scholarship_calls'}, test=can_view_scholarship_calls),
            menu.PassTestNode(id='fellowship_calls', label='Fellowship Calls', pattern_name='calls:fellowship-list',
                              link_attrs={'id': 'fellowship_calls'}, test=can_view_fellowship_calls),

        ]
    ),
    menu.PassTestNode(id='applicants', label='Interns', pattern_name='PI:applicant_list',
                      link_attrs={'id': 'applicants'}, test=can_view_applicants),
    menu.PassTestNode(
        id='students-section',
        label='Students',
        url='#',
        test=can_view_applicants,
        template='navutils/pi_students_dropdown.html',

        children = [
             menu.Node(id='all_pi_students', label='All Students', pattern_name='PI:student_list',  link_attrs={'id': 'all_pi_students'}),
             menu.Node(id='pi_students', label='My Students', pattern_name='PI:enrolled_students',  link_attrs={'id': 'enrolledstudents'}),

        ]
    ),

    # commented out for now
    # menu.PassTestNode(
    #     id='scholarship-review-section',
    #     label='Scholarship Application Review',
    #     url='#',
    #     template='navutils/dropdown.html',
    #     test=can_review_scholarships,
    #     children = [
    #
    #         menu.PassTestNode(id='other_reviews', label='Research and Innovation', pattern_name='scholarships:review_list', link_attrs={'id': 'other_reviews'}, test=can_review_scholarships),

    #     ]
    # ),
    menu.PassTestNode(
        id='grants-section',
        label='Grants',
        url='#',
        template='navutils/grants_dropdown.html',
        test=can_view_grants,
        children=[

            menu.PassTestNode(id='grants_applications',
                              label='Grant Applications',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='grants_applications:list', test=can_view_grant_applications),

            menu.PassTestNode(id='grant_applications_validation', label='Grant Application Validation',
                              pattern_name='grants_applications:validation_list',
                              link_attrs={'id': 'grant_applications_validation'}, test=can_validate_applications),
            menu.PassTestNode(id='grant_applications_validated', label='Validated Grant Application',
                              pattern_name='grants_applications:validated_list',
                              link_attrs={'id': 'grant_applications_validated'}, test=is_grant_team_member),
            menu.PassTestNode(id='grant_applications_review', label='Grant Application Review',
                              pattern_name='grants_applications:review_list',
                              link_attrs={'id': 'grant_applications_review'}, test=can_review_applications),
            menu.PassTestNode(id='grant_applications_reviewed', label='Reviewed Grant Application',
                              pattern_name='grants_applications:reviewed_list',
                              link_attrs={'id': 'grant_applications_reviewed'}, test=can_review_applications),
            menu.PassTestNode(id='grant_applications_decision', label='Application Decision',
                              pattern_name='grants_applications:application_decision_list',
                              link_attrs={'id': 'grant_applications_decision'},
                              test=can_make_grants_applications_decision),
            menu.PassTestNode(id='pi_grants',
                              label='Grants',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='PI:pi_grant_list', test=can_view_applicants),
            menu.PassTestNode(id='grants',
                              label='Grants',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='grants:list', test=can_manage_grants),
             menu.PassTestNode(id='grants',
                              label='Project Events',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='PI:events', test=can_manage_grants),
             menu.PassTestNode(id='grants',
                              label='Project Events',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='PI:events', test=can_view_applicants),


            menu.PassTestNode(id='grant_reports',
                              label='Grant Reports',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='grants:grants_reports', test=can_view_grant_reports),

        ]
    ),
    menu.PassTestNode(id='pi_repo', label='My Reports', pattern_name='PI:reports', link_attrs={'id': 'pi_repo'},
                      test=can_view_applicants),

    menu.PassTestNode(
        id='scholarship-section',
        label='Scholarships',
        url='#',
        template='navutils/scholarship_dropdown.html',
        test=can_view_scholarships,
        children=[

            menu.PassTestNode(id='scholarships',
                              label='Scholarship Application',
                              link_attrs={'class': 'dropdown-menu', 'id': 'template_manager'},
                              pattern_name='scholarships:list',
                              test=can_manage_scholarships,
                              ),
            menu.PassTestNode(id='scholarships',
                              label='Scholarship Application Validations',
                              link_attrs={'class': 'dropdown-menu', 'id': 'template_manager'},
                              pattern_name='scholarships:validation_list',
                              test=can_review_scholarships,
                              ),
            menu.PassTestNode(id='scholarship_review', label=' Scholarship Applications Review',
                              pattern_name='scholarships:mastercard_review_list',
                              link_attrs={'id': 'scholarships_review'}, test=can_review_scholarships),
            menu.PassTestNode(id='scholarship_reviewed', label='Reviewed Scholarship Applications ',
                              pattern_name='scholarships:reviewed_scholarships_list',
                              link_attrs={'id': 'scholarships_reviewed'}, test=can_review_scholarships),
            menu.PassTestNode(id='application_decision', label='Applications Decision',
                              pattern_name='scholarships:scholarship_application_decision_list',
                              link_attrs={'id': 'scholarships_decision'}, test=can_make_scholarships_decisions),
            menu.PassTestNode(id='awarded_scholarships', label='Scholarships',
                              pattern_name='scholarships:scholarship_list', link_attrs={'id': 'awarded_scholarships'},
                              test=can_review_scholarships),
            menu.PassTestNode(id='my_student_reports', label='Submit Reports',
                              pattern_name='student_reports:my_reports', link_attrs={'id': 'my_student_reports'},
                              test=is_student),
            menu.PassTestNode(id='my_reports', label='My Reports', pattern_name='student_reports:my_student_reports',
                              link_attrs={'id': 'my_reports'}, test=is_student),
            # menu.PassTestNode(id='mastercard_reviews', label='Mastercard', pattern_name='scholarships:mastercard_review_list', link_attrs={'id': 'mastercard_reviews'}, test=can_review_scholarships),
            menu.PassTestNode(id='student_reports', label='Student Reports', pattern_name='student_reports:list',
                              link_attrs={'id': 'student_reports'}, test=can_manage_student_reports),
        ]
    ),
    menu.PassTestNode(
        id='fellowship-section',
        label='Fellowships',
        url='#',
        template='navutils/fellowship_dropdown.html',
        test=can_view_fellowship,
        children=[
            # menu.PassTestNode(id='fellowship',
            #           label='Fellowships',
            #           link_attrs={'class': 'dropdown-menu'},
            #           pattern_name='fellowship:list',test=can_manage_fellowship),
            menu.PassTestNode(id='fellowship_applications',
                              label='Fellowship Applications',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='fellowship_applications:list', test=can_view_fellowship),
            menu.PassTestNode(id='fellowship_applications_validation', label='Fellowship Application Validation',
                              pattern_name='fellowship_applicationss:validation_list',
                              link_attrs={'id': 'grant_applications_validation'}, test=can_validate_fellowship_applications),
            menu.PassTestNode(id='fellowship_applications_validated', label='Fellowship Application Review',
                           pattern_name='fellowship_applicationss:review_list',
                              link_attrs={'id': 'fellowship_applications_validated'}, test=can_view_fellowship),
            menu.PassTestNode(id='fellowship_applications_reviewed', label='Reviewed Fellowship Application',
                              pattern_name='fellowship_applicationss:reviewed_list',
                              link_attrs={'id': 'grant_applications_review'}, test=can_review_applications),
            # menu.PassTestNode(id='grant_applications_reviewed', label='Reviewed Fellowship Application',
            #                   pattern_name='fellowship_applicationss:reviewed_list',
            #                   link_attrs={'id': 'grant_applications_reviewed'}, test=can_review_applications),
            # menu.PassTestNode(id='grant_applications_decision', label='Application Decision',
            #                   pattern_name='fellowship_applicationss:application_decision_list',
            #                   link_attrs={'id': 'grant_applications_decision'},
            #                   test=can_make_grants_applications_decision),
            
            menu.PassTestNode(id='grants',
                              label='Fellowships',
                              link_attrs={'class': 'dropdown-menu'},
                              pattern_name='grants:list', test=can_manage_grants),


        ]
    ),
    # hr menu
    menu.PassTestNode(
        id='hr-section',
        label='HR',
        url='#',
        template='navutils/hr_dropdown.html',
        test=can_manage_users,
        children=[
            menu.PassTestNode(id='documents', label='Documents', pattern_name='common:doc_list',
                              link_attrs={'id': 'documents'}, test=can_manage_users),
            menu.PassTestNode(id='departments', label='Departments', pattern_name='hrm:department_list',
                              link_attrs={'id': 'dept_list'}, test=can_manage_users),
            menu.PassTestNode(id='staff', label='Staff', pattern_name='hrm:staff_list', link_attrs={'id': 'staff'},
                              test=can_manage_users),
            menu.PassTestNode(id='leaves', label='Leave', pattern_name='hrm:leave_list', link_attrs={'id': 'leaves'},
                              test=can_manage_users),
            menu.PassTestNode(id='events', label='Events', pattern_name='events:list', link_attrs={'id': 'events'},
                              test=can_manage_users),
            menu.PassTestNode(id='travels', label='Travel', pattern_name='hrm:travel_list',
                              link_attrs={'id': 'travels'}, test=can_manage_users),
            menu.PassTestNode(id='asset_categories', label='Asset Categories', pattern_name='hrm:asset_category_list',
                              link_attrs={'id': 'asset_category_list'}, test=can_manage_users),
            menu.PassTestNode(id='assets', label='Assets', pattern_name='hrm:asset_list',
                              link_attrs={'id': 'asset_list'}, test=can_manage_users),
            menu.PassTestNode(id='vehicles', label='Vehicles', pattern_name='hrm:vehicle_list',
                              link_attrs={'id': 'vehicles'}, test=can_manage_users),
            menu.PassTestNode(id='calendar', label='Calendar', pattern_name='hrm:calendar',
                              link_attrs={'id': 'calendar'}, test=can_manage_users),

            menu.PassTestNode(id='tasks', label='Tasks', pattern_name='tasks:tasks_list', link_attrs={'id': 'tasks'},
                              test=can_manage_users),
            menu.PassTestNode(id='id_contracts', label='Contracts', pattern_name='hrm:contract_list',
                              link_attrs={'id': 'contract'}, test=can_manage_users),
        ]
    ),
    # m& E menu
    menu.PassTestNode(
        id='EandE-section',
        label='M & E',
        url='#',
        template='navutils/pme_dropdown.html',
        test=can_manage_users,
        children=[
            menu.PassTestNode(id='workplan', label='Work Plans', pattern_name='pme:workplan_list',
                              link_attrs={'id': 'work_plans'}, test=can_manage_users),
            menu.PassTestNode(id='activities',
                              label='Activities',
                              link_attrs={'class': 'dropdown-menu', 'id': 'activities'},
                              pattern_name='pme:activity_list',
                              test=can_manage_users,
                              ),
            menu.PassTestNode(id='expected_out_put', label='Activity Expected Outputs', pattern_name='pme:output_list',
                              link_attrs={'id': 'expected_out_put'}, test=can_manage_users),
            menu.PassTestNode(id='indicators', label='Activity Indicators', pattern_name='pme:indicator_list',
                              link_attrs={'id': 'Indicators'}, test=can_manage_users),
            menu.PassTestNode(id='out_put', label='Activity Output', pattern_name='pme:activity_output_list',
                              link_attrs={'id': 'outputs'}, test=can_manage_users),
            menu.PassTestNode(id='tasks',
                              label='Tasks',
                              link_attrs={'class': 'dropdown-menu', 'id': 'tasks'},
                              pattern_name='pme:task_list',
                              test=can_manage_users,
                              ),
            menu.PassTestNode(id='task_reports', label='Task Reports', pattern_name='pme:task_reports',
                              link_attrs={'id': 'task_report'}, test=can_manage_users),
            menu.PassTestNode(id='unit_of_measurement_me',
                              label='Unit of measurement',
                              link_attrs={'class': 'dropdown-menu', 'id': 'tasks'},
                              pattern_name='pme:framework_unit_list',
                              test=can_manage_users,
                              ),
            menu.PassTestNode(id='framework_list', label='Results Area', pattern_name='pme:framework_list',
                              link_attrs={'id': 'framework_list'}, test=can_manage_users),
            menu.PassTestNode(id='framework_result_list', label='Results', pattern_name='pme:framework_result_list',
                              link_attrs={'id': 'framework_result_list'}, test=can_manage_users),
            menu.PassTestNode(id='unt_s',
                              label='Units',
                              link_attrs={'class': 'dropdown-menu', 'id': 'units-s'},
                              pattern_name='pme:unit_list',
                              test=can_manage_users,
                              ),
            menu.PassTestNode(id='framework_list', label='Development partner', pattern_name='pme:sourceoffunding_list',
                              link_attrs={'id': 'framework_list'}, test=can_manage_users),
            menu.PassTestNode(id='resultarea_list', label='Ruforum flagship program',
                              pattern_name='pme:resultarea_list', link_attrs={'id': 'resultarea_list'},
                              test=can_manage_users),
            menu.PassTestNode(id='financialyear_list', label='Financial Years', pattern_name='pme:financialyear_list',
                              link_attrs={'id': 'financialyear_list'}, test=can_manage_users),

        ]
    ),

     menu.PassTestNode(
        id='projects-management',
        label='Projects',
        url='#',
        template='navutils/users_dropdown.html',
        test=is_project_manager,
        children=[
            menu.Node(id='projects',
                      label='Ruforum Projects',
                      link_attrs={'class': 'dropdown-menu'},
                      pattern_name='project_management:projectlist'),
            menu.Node(id='groups',
                      label='Project Frameworks',
                      link_attrs={'class': 'dropdown-menu'},
                      pattern_name='project_management:activitieslist'),
        ]
    ),

    menu.PassTestNode(
        id='users-section',
        label='Users',
        url='#',
        template='navutils/users_dropdown.html',
        test=can_manage_users,
        children=[
            menu.Node(id='users',
                      label='Users',
                      link_attrs={'class': 'dropdown-menu'},
                      pattern_name='common:users_list'),
            menu.Node(id='groups',
                      label='User Groups',
                      link_attrs={'class': 'dropdown-menu'},
                      pattern_name='common:groups_list'),
        ]
    ),


    menu.PassTestNode(
        id='settings-section',
        label='Settings',
        url='#',
        template='navutils/settings_dropdown.html',
        test=can_manage_settings,
        children=[
            menu.Node(id='templates',
                      label='Templates',
                      link_attrs={'class': 'dropdown-menu'},
                      pattern_name='template_manager:list'),
        ]
    ),
    menu.PassTestNode(id='events1', label='Events', pattern_name='events:list', link_attrs={'id': 'events1'},
                      test=is_view_and_add_contacts_manager),
    menu.PassTestNode(id='workplan', label='Work Plans', pattern_name='pme:workplan_list',
                      link_attrs={'id': 'work_plans'}, test=is_pmeuser),
    menu.PassTestNode(id='activities-section', label='Activities', url='#',
                      template='navutils/dropdown.html',
                      test=is_pmeuser,
                      children=[

                          menu.PassTestNode(id='activities',
                                            label='Activities',
                                            link_attrs={'class': 'dropdown-menu', 'id': 'activities'},
                                            pattern_name='pme:activity_list',
                                            test=is_pmeuser,
                                            ),
                          menu.PassTestNode(id='expected_out_put', label='Expected Outputs',
                                            pattern_name='pme:output_list', link_attrs={'id': 'expected_out_put'},
                                            test=is_pmeuser),
                          menu.PassTestNode(id='indicators', label='Indicators', pattern_name='pme:indicator_list',
                                            link_attrs={'id': 'Indicators'}, test=is_pmeuser),
                          menu.PassTestNode(id='out_put', label='Output', pattern_name='pme:activity_output_list',
                                            link_attrs={'id': 'outputs'}, test=is_pmeuser),

                      ]
                      ),

    menu.PassTestNode(id='tasks-section', label='Tasks', url='#',
                      template='navutils/dropdown.html',
                      test=is_pmeuser,
                      children=[

                          menu.PassTestNode(id='tasks',
                                            label='Tasks',
                                            link_attrs={'class': 'dropdown-menu', 'id': 'tasks'},
                                            pattern_name='pme:task_list',
                                            test=is_pmeuser,
                                            ),
                          menu.PassTestNode(id='task_reports', label='Reports', pattern_name='pme:task_reports',
                                            link_attrs={'id': 'task_report'}, test=is_pmeuser),

                      ]
                      ),

    menu.PassTestNode(id='framework-section', label=' M & E Framework', url='#',
                      template='navutils/dropdown.html',
                      test=is_pmeuser,
                      children=[

                          menu.PassTestNode(id='unit_of_measurement_me',
                                            label='Unit of measurement',
                                            link_attrs={'class': 'dropdown-menu', 'id': 'tasks'},
                                            pattern_name='pme:framework_unit_list',
                                            test=is_pmeuser,
                                            ),
                          menu.PassTestNode(id='framework_list', label='Results Area',
                                            pattern_name='pme:framework_list', link_attrs={'id': 'framework_list'},
                                            test=is_pmeuser),
                          menu.PassTestNode(id='framework_result_list', label='Results',
                                            pattern_name='pme:framework_result_list',
                                            link_attrs={'id': 'framework_result_list'}, test=is_pmeuser),

                      ]
                      ),
    menu.PassTestNode(id='pme_settings-section', label='Settings', url='#',
                      template='navutils/dropdown.html',
                      test=is_pmeuser,
                      children=[

                          menu.PassTestNode(id='unt_s',
                                            label='Units',
                                            link_attrs={'class': 'dropdown-menu', 'id': 'units-s'},
                                            pattern_name='pme:unit_list',
                                            test=is_pmeuser,
                                            ),
                          menu.PassTestNode(id='framework_list', label='Development partner',
                                            pattern_name='pme:sourceoffunding_list',
                                            link_attrs={'id': 'framework_list'}, test=is_pmeuser),
                          menu.PassTestNode(id='resultarea_list', label='Ruforum flagship program',
                                            pattern_name='pme:resultarea_list', link_attrs={'id': 'resultarea_list'},
                                            test=is_pmeuser),
                          menu.PassTestNode(id='financialyear_list', label='Financial Years',
                                            pattern_name='pme:financialyear_list',
                                            link_attrs={'id': 'financialyear_list'}, test=is_pmeuser),

                      ]
                      ),
    menu.PassTestNode(id='documents', label='Documents', pattern_name='common:doc_list', link_attrs={'id': 'documents'},
                      test=is_hr_manager),
    menu.PassTestNode(
        id='organization-section',
        label='Organization',
        url='#',
        template='navutils/dropdown.html',
        test=is_hr_manager,
        children=[
            menu.PassTestNode(id='departments', label='Departments', pattern_name='hrm:department_list',
                              link_attrs={'id': 'dept_list'}, test=is_hr_manager),
        ]
    ),
    menu.PassTestNode(id='staff', label='Staff', pattern_name='hrm:staff_list', link_attrs={'id': 'staff'},
                      test=is_hr_manager),

    menu.PassTestNode(
        id='leaves',
        label='Leave',
        url='#',
        template='navutils/dropdown.html',
        test=can_view_leave,
        children=[
            menu.PassTestNode(id='leave_type', label='Leave Type', pattern_name='hrm:leave_list',
                              link_attrs={'id': 'leave_type'}, test=can_view_leave),
            menu.PassTestNode(id='leave_assignment', label='Leave Assignments', pattern_name='hrm:leave_assignments',
                              link_attrs={'id': 'leave_assignments'}, test=can_view_leave),

            menu.PassTestNode(id='leave_applications', label='Leave Applications', pattern_name='hrm:leave_applications',
                              link_attrs={'id': 'applications'}, test=can_view_leave_applications),
                              
            menu.PassTestNode(id='leaves', label='Leaves', pattern_name='hrm:approved_leaves',
                              link_attrs={'id': 'leaves'}, test=can_view_leave_applications),
        ]
    ),
      menu.PassTestNode(
        id='appraisals',
        label='Appraisals',
        url='#',
        template='navutils/dropdown.html',
        test=can_view_appraisals,
        children=[
            menu.PassTestNode(id='month6Appraisal', label='Six Monthly Staff Performance Report', pattern_name='hrm:month6_appraisals',
                              link_attrs={'id': 'leave_type'}, test=can_view_appraisals),
            # menu.PassTestNode(id='leave_assignment', label='Leave Assignments', pattern_name='hrm:leave_assignments',
            #                   link_attrs={'id': 'leave_assignments'}, test=is_hr_manager),

            # menu.PassTestNode(id='leave_applications', label='Leave Applications', pattern_name='hrm:leave_applications',
            #                   link_attrs={'id': 'applications'}, test=can_view_leave_applications),
                              
            # menu.PassTestNode(id='leaves', label='Leaves', pattern_name='hrm:approved_leaves',
            #                   link_attrs={'id': 'leaves'}, test=can_view_leave_applications),
        ]
    ),
    menu.PassTestNode(id='events', label='Events', pattern_name='events:list', link_attrs={'id': 'events'},
                      test=is_hr_manager),
    menu.PassTestNode(id='travels', label='Travel', pattern_name='hrm:travel_list', link_attrs={'id': 'travels'},
                      test=is_hr_manager),
    menu.PassTestNode(
        id='asset-section',
        label='Assets',
        url='#',
        template='navutils/dropdown.html',
        test=is_hr_manager,
        children=[
            menu.PassTestNode(id='asset_categories', label='Asset Categories', pattern_name='hrm:asset_category_list',
                              link_attrs={'id': 'asset_category_list'}, test=is_hr_manager),
            menu.PassTestNode(id='assets', label='Assets', pattern_name='hrm:asset_list',
                              link_attrs={'id': 'asset_list'}, test=is_hr_manager),
        ]
    ),
    menu.PassTestNode(id='vehicles', label='Vehicles', pattern_name='hrm:vehicle_list', link_attrs={'id': 'vehicles'},
                      test=is_hr_manager),
    menu.PassTestNode(id='calendar', label='Calendar', pattern_name='hrm:calendar', link_attrs={'id': 'calendar'},
                      test=is_hr_manager),
    menu.PassTestNode(id='tasks', label='Tasks', pattern_name='tasks:tasks_list', link_attrs={'id': 'tasks'},
                      test=is_hr_manager),
    menu.PassTestNode(id='id_contracts', label='Contracts', pattern_name='hrm:contract_list',
                      link_attrs={'id': 'contract'}, test=is_hr_manager),

]

for entry in menus:
    main_menu.register(entry)
