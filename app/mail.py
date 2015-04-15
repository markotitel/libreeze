__author__ = 'nmilinkovic'

import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

logger = logging.getLogger(__name__)

def send_verification_email(to_email, verification_code):

    logger.debug("Sending verification email to %s" % to_email)

    subject = 'Verify your email address'
    from_email = 'libreeze@libreeze.net'

    verification_plaintext = get_template('app/email/verification.txt')
    verification_html = get_template('app/email/verification.html')

    context = Context({'verification_code': verification_code})

    text_content = verification_plaintext.render(context)
    html_content = verification_html.render(context)

    message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_update_email(to_email, project, dependencies):

    logger.debug("Sending update email to %s for project %s" % (to_email, project))

    subject = 'New library versions available for ' + project.name
    from_email = 'libreeze@libreeze.net'

    plaintext_template = get_template('app/email/dependencies.txt')
    html_template = get_template('app/email/dependencies.html')

    context = Context({'project': project, 'dependencies': dependencies})

    text_content = plaintext_template.render(context)
    html_content = html_template.render(context)

    message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    message.attach_alternative(html_content, "text/html")
    message.send()

