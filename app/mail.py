__author__ = 'nmilinkovic'

from django.core.mail import send_mail

def send_subscription_notification(maven_project):
    send_mail('project subscribed',
              'you will be receiving updates soon',
              'no-reply@libreeze.net',
              maven_project.developer.email)