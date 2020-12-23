from datetime import date,timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from grants.models import Grant
from django.core.mail import EmailMessage
from grants_reports.models import (Studentmonth6Report, Month12Report, Month12Report, Month18Report, Month24Report,
                                   Month30Report, Studentmonth12Report, Studentmonth18Report,
                                   Studentmonth24Report, Studentmonth30Report)

from dateutil.relativedelta import relativedelta
def run():
    # find grants that have start date from now
    grants=Grant.objects.filter(end_date__lte = date.today())

    for grant in grants:
        periods=[]
        if grant.reporting_period==3: periods = Grant.PERIOD_CHOICES[:grant.report_number]
        if grant.reporting_period==6: periods = Grant.PERIOD_CHOICES6[:grant.report_number]
        if grant.pi is not None:
            name =grant.pi.first_name+ " "+grant.pi.last_name
            pi_email=grant.pi.business_email
        for (n,period) in enumerate(periods):
            try:
                month6grrantreport=Month12Report.objects.filter(grant=grant)
                if n==0 and not month6grrantreport and grant.start_date+relativedelta(months=grant.reporting_period-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                if n==0 and not month6grrantreport and grant.start_date+relativedelta(weeks=2)+relativedelta(months=grant.reporting_period-1)== date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                if n==0 and not month6grrantreport and grant.start_date+relativedelta(months=grant.reporting_period-1)+relativedelta(weeks=3) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                    

                month12grrantreport=Month12Report.objects.filter(grant=grant)
                if n==1 and not month12grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*2)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)

                if n==1 and not month12grrantreport and grant.start_date+relativedelta(weeks=2)+relativedelta(months=(grant.reporting_period*2)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                
                if n==1 and not month12grrantreport and grant.start_date+relativedelta(weeks=3)+relativedelta(months=(grant.reporting_period*2)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                    

                month18grrantreport=Month18Report.objects.filter(grant=grant)
                if n==2 and not month18grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*3)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                if n==2 and not month18grrantreport and grant.start_date+relativedelta(weeks=2)+relativedelta(months=(grant.reporting_period*3)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                
                if n==2 and not month18grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*3)-1)+relativedelta(weeks=3) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                    

                month24grrantreport=Month24Report.objects.filter(grant=grant)
                if n==3 and not month24grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*4)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                if n==3 and not month24grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*4)-1)+relativedelta(weeks=2) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                
                if n==3 and not month24grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*4)-1)+relativedelta(weeks=3) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                    

                month30grrantreport=Month30Report.objects.filter(grant=grant)
                if n==4 and not month30grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*5)-1) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                
                if n==4 and not month30grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*5)-1)+relativedelta(weeks=2) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                
                if n==4 and not month30grrantreport and grant.start_date+relativedelta(months=(grant.reporting_period*5)-1)+relativedelta(weeks=3) == date.today():
                    mail_subject = 'Ruforum PI '+period[1]+' Report'
                    message = "Dear "+name+", <br> You are hereby reminded to submit your "+period[1]+" Grant Report."
                    email = EmailMessage(mail_subject, message, to=[pi_email],from_email="nonereply@ruforum.org")
                    email.content_subtype = "html"
                    email.send()
                    print(message)
                   

            except Grant.DoesNotExist:
                grant = None






