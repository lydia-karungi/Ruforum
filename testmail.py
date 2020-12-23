# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
API_KEY = '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'
message = Mail(
    from_email='admin@ruforum.org',
    to_emails='joshuamasiko@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(API_KEY) #os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
