from django.urls import path, include
from grants_reports.views import (
    PIreportsListView, CreatePireportView, SavePireportView, CreatePi12MonthreportView, SavePi12MonthreportView
, CreatePi18MonthreportView, SavePi18MonthreportView, CreatePi24MonthreportView, SavePi24MonthreportView,
    CreatePi30MonthreportView, SavePi30MonthreportView
, CreatePi30MonthreportView, SavePi30MonthreportView, CreatePi36MonthreportView, SavePi36MonthreportView,
    CreatePiLastreportView, SavePiLastreportView, CreatePi42MonthReportView, SavePi42MonthReportView,
    CreatePi48MonthReportView, SavePi48MonthReportView, CreatePi54MonthReportView, SavePi54MonthReportView,
    SavePi60MonthReportView, CreatePi60MonthReportView, CreatePi66MonthReportView, SavePi66MonthReportView,
    SavePi72MonthReportView, CreatePi72MonthReportView, CreatePi78MonthReportView, SavePi78MonthReportView,
    SavePi84MonthReportView, CreatePi84MonthReportView, SavePi90MonthReportView, CreatePi90MonthReportView,
    SavePi96MonthReportView, CreatePi96MonthReportView, SavePi102MonthReportView, CreatePi102MonthReportView,
    CreatePi108MonthReportView, SavePi108MonthReportView,AcceptFirstReportView, AcceptSecondReportView,
    AcceptThirdReportView,AcceptFourthReportView,AcceptFifthReportView,AcceptSixthReportView,
    AcceptSeventhReportView,AcceptNineththReportView,AcceptEighthReportView,AcceptEleventhReportView,
    AcceptTenthReportView, AcceptTwelvethReportView, AcceptThirteenthReportView, AcceptFourteenthReportView,
    AcceptFifteenthReportView, AcceptSixteenthReportView, AcceptSeventeenthReportView, AcceptEighteenthReportView,
    AcceptLastReportView, UpdateFirstPIView,Edit12MonthreportView,Edit18MonthreportView,Edit24MonthreportView,
    Edite30MonthreportView,Edite36MonthreportView,Edite42MonthreportView,Edite48MonthreportView,Edite54MonthreportView
    ,Edite60MonthreportView,Edite66MonthreportView,Edite72MonthreportView,Edite78MonthreportView,Edite84MonthreportView,
    Edite90MonthreportView,Edite96MonthreportView,Edite102MonthreportView,Edite108MonthreportView,EditPiLastreportView
)
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'reports', views.ReportsViewSet)



app_name = 'grants_reports'


urlpatterns = [
    path('api/', include(router.urls)),
    path('<int:pk>/pi_reports', PIreportsListView.as_view(), name='pi_reports'),
    #  path('student/reports', SingleStudentreportsListView.as_view(), name='my_student_reports'),
    path('3/<int:pk>/6 Months/create/', CreatePireportView.as_view(), name='add_pi_report'),
    path('save/6month/report/', SavePireportView.as_view(), name="save_six_month_report"),
    path('3/<int:pk>/3 Months/create/', CreatePireportView.as_view(), name='add_pi_3months_report'),
    path('<int:pk>/edit/3/6/report/',UpdateFirstPIView.as_view(), name='edit_pi_3month_report'),

    path('6/<int:pk>/12 Months/create/', CreatePi12MonthreportView.as_view(), name='add_pi_12Month_report'),
    path('save/12month/report/', SavePi12MonthreportView.as_view(), name="save_Twelve_month_report"),
    path('6/<int:pk>/6 Months/create/', CreatePi12MonthreportView.as_view(), name='add_pi_12months_report'),
    path('<int:pk>/edit/6/12/report/',Edit12MonthreportView.as_view(), name='edit_pi_6month_report'),

    path('9/<int:pk>/18 Months/create/', CreatePi18MonthreportView.as_view(), name='add_pi_18Month_report'),
    path('save/18month/report/', SavePi18MonthreportView.as_view(), name="save_eighteen_month_report"),
    path('9/<int:pk>/9 Months/create/', CreatePi18MonthreportView.as_view(), name='add_pi_18months_report'),
    path('<int:pk>/edit/9/18/report/',Edit18MonthreportView.as_view(), name='edit_pi_9month_report'),

    path('12/<int:pk>/24 Months/create/', CreatePi24MonthreportView.as_view(), name='add_pi_24Month_report'),
    path('save/24month/report/', SavePi24MonthreportView.as_view(), name="save_twenty_four_month_report"),
    path('12/<int:pk>/12 Months/create/', CreatePi24MonthreportView.as_view(), name='add_pi_24months_report'),
    path('<int:pk>/edit/12/24/report/',Edit24MonthreportView.as_view(), name='edit_pi_12month_report'),


    path('15/<int:pk>/30 Months/create/', CreatePi30MonthreportView.as_view(), name='add_pi_30Month_report'),
    path('save/30month/report/', SavePi30MonthreportView.as_view(), name="save_thirty_month_report"),
    path('15/<int:pk>/15 Months/create/', CreatePi30MonthreportView.as_view(), name='add_pi_30months_report'),
    path('<int:pk>/edit/15/30/report/',Edite30MonthreportView.as_view(), name='edit_pi_15month_report'),

    path('18/<int:pk>/36 Months/create/', CreatePi36MonthreportView.as_view(), name='add_pi_36Month_report'),
    path('save/36month/report/', SavePi36MonthreportView.as_view(), name="save_thirty_six_month_report"),
    path('18/<int:pk>/18 Months/create/', CreatePi36MonthreportView.as_view(), name='add_pi_36months_report'),
    path('<int:pk>/edit/18/36/report/',Edite36MonthreportView.as_view(), name='edit_pi_18month_report'),

    path('21/<int:pk>/42 Months/create/', CreatePi42MonthReportView.as_view(), name='add_pi_42Month_report'),
    path('save/42month/report/', SavePi42MonthReportView.as_view(), name="save_forty_two_month_report"),
    path('21/<int:pk>/21 Months/create/', CreatePi42MonthReportView.as_view(), name='add_pi_42months_report'),
    path('<int:pk>/edit/21/42/report/',Edite42MonthreportView.as_view(), name='edit_pi_21month_report'),

    path('24/<int:pk>/48 Months/create/', CreatePi48MonthReportView.as_view(), name='add_pi_48Month_report'),
    path('save/48month/report/', SavePi48MonthReportView.as_view(), name='save_forty_eight_month_report'),
    path('24/<int:pk>/24 Months/create/', CreatePi48MonthReportView.as_view(), name='add_pi_48months_report'),
    path('<int:pk>/edit/24/48/report/',Edite48MonthreportView.as_view(), name='edit_pi_24month_report'),

    path('27/<int:pk>/54 Months/create/', CreatePi54MonthReportView.as_view(), name='add_pi_54Month_report'),
    path('save/54month/report/', SavePi54MonthReportView.as_view(), name="save_fifty_four_month_report"),
    path('27/<int:pk>/27 Months/create/', CreatePi54MonthReportView.as_view(), name='add_pi_54months_report'),
    path('<int:pk>/edit/27/54/report/',Edite54MonthreportView.as_view(), name='edit_pi_27month_report'),

    path('30/<int:pk>/60 Months/create/', CreatePi60MonthReportView.as_view(), name='add_pi_60Month_report'),
    path('save/60month/report/', SavePi60MonthReportView.as_view(), name="save_sixty_month_report"),
    path('30/<int:pk>/30 Months/create/', CreatePi60MonthReportView.as_view(), name='add_pi_60months_report'),
    path('<int:pk>/edit/30/60/report/',Edite60MonthreportView.as_view(), name='edit_pi_30month_report'),

    path('33/<int:pk>/66 Months/create/', CreatePi66MonthReportView.as_view(), name='add_pi_42Month_report'),
    path('save/66month/report/', SavePi66MonthReportView.as_view(), name="save_sixty_six_month_report"),
    path('33/<int:pk>/33 Months/create/', CreatePi66MonthReportView.as_view(), name='add_pi_42months_report'),
    path('<int:pk>/edit/33/66/report/',Edite66MonthreportView.as_view(), name='edit_pi_33month_report'),

    path('36/<int:pk>/72 Months/create/', CreatePi72MonthReportView.as_view(), name='add_pi_72Month_report'),
    path('save/72month/report/', SavePi72MonthReportView.as_view(), name="save_seventy_two_month_report"),
    path('36/<int:pk>/36 Months/create/', CreatePi72MonthReportView.as_view(), name='add_pi_72months_report'),
    path('<int:pk>/edit/36/72/report/',Edite72MonthreportView.as_view(), name='edit_pi_36month_report'),

    path('39/<int:pk>/78 Months/create/', CreatePi78MonthReportView.as_view(), name='add_pi_78Month_report'),
    path('save/78month/report/', SavePi78MonthReportView.as_view(), name="save_seventy_eight_month_report"),
    path('39/<int:pk>/39 Months/create/', CreatePi78MonthReportView.as_view(), name='add_pi_78months_report'),
    path('<int:pk>/edit/39/78/report/',Edite78MonthreportView.as_view(), name='edit_pi_39month_report'),

    path('42/<int:pk>/84 Months/create/', CreatePi84MonthReportView.as_view(), name='add_pi_84Month_report'),
    path('save/84month/report/', SavePi84MonthReportView.as_view(), name="save_eighty_four_month_report"),
    path('42/<int:pk>/42 Months/create/', CreatePi84MonthReportView.as_view(), name='add_pi_84months_report'),
    path('<int:pk>/edit/42/84/report/',Edite84MonthreportView.as_view(), name='edit_pi_42month_report'),

    path('45/<int:pk>/90 Months/create/', CreatePi90MonthReportView.as_view(), name='add_pi_90Month_report'),
    path('save/90month/report/', SavePi90MonthReportView.as_view(), name="save_ninety_month_report"),
    path('45/<int:pk>/45 Months/create/', CreatePi90MonthReportView.as_view(), name='add_pi_90months_report'),
    path('<int:pk>/edit/45/90/report/',Edite90MonthreportView.as_view(), name='edit_pi_45month_report'),

    path('48/<int:pk>/96 Months/create/', CreatePi96MonthReportView.as_view(), name='add_pi_96Month_report'),
    path('save/96month/report/', SavePi96MonthReportView.as_view(), name="save_ninety_six_month_report"),
    path('48/<int:pk>/48 Months/create/', CreatePi96MonthReportView.as_view(), name='add_pi_96months_report'),
    path('<int:pk>/edit/48/96/report/',Edite96MonthreportView.as_view(), name='edit_pi_48month_report'),

    path('51/<int:pk>/102 Months/create/', CreatePi102MonthReportView.as_view(), name='add_pi_102Month_report'),
    path('save/102month/report/', SavePi102MonthReportView.as_view(), name="save_one_zero_two_month_report"),
    path('51/<int:pk>/51 Months/create/', CreatePi102MonthReportView.as_view(), name='add_pi_102months_report'),
    path('<int:pk>/edit/51/102/report/',Edite102MonthreportView.as_view(), name='edit_pi_51month_report'),

    path('54/<int:pk>/108 Months/create/', CreatePi108MonthReportView.as_view(), name='add_pi_108Month_report'),
    path('save/108month/report/', SavePi108MonthReportView.as_view(), name="save_one_zero_eight_month_report"),
    path('54/<int:pk>/54 Months/create/', CreatePi108MonthReportView.as_view(), name='add_pi_108months_report'),
    path('<int:pk>/edit/54/108/report/',Edite108MonthreportView.as_view(), name='edit_pi_54month_report'),

    #last report
    path('final/<int:pk>/create', CreatePiLastreportView.as_view(), name='add_pi_last_report'),
    path('save/last/report/', SavePiLastreportView.as_view(), name="save_last_report"),
    path('<int:pk>/edit/lastreport', EditPiLastreportView.as_view(), name='edit_pi_last_report'),
    #path('18/<int:pk>/15 Months/create/', CreatePiLastreportView.as_view(), name='add_pi_last_report'),
    path('<int:pk>/accept_first_report/', AcceptFirstReportView.as_view(), name="accept_first_report"),
    path('<int:pk>/accept_second_report/', AcceptSecondReportView.as_view(), name="accept_second_report"),
    path('<int:pk>/accept_third_report/', AcceptThirdReportView.as_view(), name="accept_third_report"),
    path('<int:pk>/accept_fouth_report/', AcceptFourthReportView.as_view(), name="accept_fourth_report"),
    path('<int:pk>/accept_fifth_report/', AcceptFifthReportView.as_view(), name="accept_fifth_report"),
    path('<int:pk>/accept_sixth_report/', AcceptSixthReportView.as_view(), name="accept_sixth_report"),
    path('<int:pk>/accept_seventh_report/', AcceptSeventhReportView.as_view(), name="accept_seventh_report"),
    path('<int:pk>/accept_eighth_report/', AcceptEighthReportView.as_view(), name="accept_eighth_report"),
    path('<int:pk>/accept_nineth_report/', AcceptNineththReportView.as_view(), name="accept_nineth_report"),
    path('<int:pk>/accept_tenth_report/', AcceptTenthReportView.as_view(), name="accept_tenth_report"),
    path('<int:pk>/accept_eleventh_report/', AcceptEleventhReportView.as_view(), name="accept_elventh_report"),
    path('<int:pk>/accept_twelveth_report/', AcceptTwelvethReportView.as_view(), name="accept_twelveth_report"),
    path('<int:pk>/accept_thirteenth_report/', AcceptThirteenthReportView.as_view(), name="accept_thirteenth_report"),
    path('<int:pk>/accept_fourteenth_report/', AcceptFourteenthReportView.as_view(), name="accept_fourteenth_report"),
    path('<int:pk>/accept_fifteenth_report/', AcceptFifteenthReportView.as_view(), name="accept_fifteenth_report"),
    path('<int:pk>/accept_sixteenth_report/', AcceptSixteenthReportView.as_view(), name="accept_sixteenth_report"),
    path('<int:pk>/accept_seventeenth_report/', AcceptSeventeenthReportView.as_view(), name="accept_seventeenth_report"),
    path('<int:pk>/accept_eighteenth_report/', AcceptEighteenthReportView.as_view(), name="accept_eighteenth_report"),
    path('<int:pk>/accept_last_report/', AcceptLastReportView.as_view(), name="accept_last_report"),
    # path('<int:pk>/delete/',
    #      StudentreportDeleteView.as_view(),
    #      name="remove_student_report"),
]
