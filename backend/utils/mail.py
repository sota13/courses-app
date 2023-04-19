import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import environ
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SENDGRID_API_KEY=env("SENDGRID_API_KEY")

class Sender:
    @staticmethod
    def send_email(data):
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email("admin@m.tidycourse.com")
        to_email = To(data['to'])
        subject = data['subject']
        content = Content("text/plain", data['content'])
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()

        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)