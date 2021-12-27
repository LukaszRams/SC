from django.core.mail import EmailMessage
from .models import Club, User


class Email:
    """
    Email class
    """
    def __init__(self, subject, html_content, recipient_list, sender, attachement=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        self.attachement = attachement

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        if self.attachement:
            msg.attach(self.attachement.name, self.attachement.read(), self.attachement.content_type)
        msg.send(fail_silently=False)


def send_html_mail(subject, html_content, recipient_list, sender, attachement=None):
    Email(subject, html_content, recipient_list, sender, attachement).run()


def check_if_user_exist(username):
    """
    Return Club object if username is correct else None
    :param username:
    :return:
    """
    try:
        user = Club.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user
