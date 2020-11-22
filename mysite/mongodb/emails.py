# emails.py

from django.template import loader
from django.core.mail import EmailMultiAlternatives

from django.conf import settings


class NotificationEmail:
    subject_template_name = "mongodb/email/action_notification_subject.txt"
    email_template_name = "mongodb/email/action_notification_email.txt"
    from_email = settings.MONGODB_FROM_EMAIL
    to_email = settings.MONGODB_TO_EMAIL

    def send_mail(self, context):
        subject = loader.render_to_string(
            self.subject_template_name, context
        )
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            self.email_template_name, context
        )
        email_message = EmailMultiAlternatives(
            subject, body, self.from_email, self.to_email
        )
        email_message.send()

mongodb_notification_email = NotificationEmail()
