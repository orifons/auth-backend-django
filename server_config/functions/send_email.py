from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(template_name, context, subject, to_mail):
    """ Send an e-mail message with a subject and a message. """
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, None, [to_mail])
    email.attach_alternative(html_content, "text/html")
    email.send()
