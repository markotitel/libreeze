import uuid
import re

from datetime import datetime

from django.shortcuts import render

from app.controller import process_pom_file
from app.models import Developer
from app.mail import send_verification_email


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Create your views here.


def index(request):
    # TODO move to static
    return render(request, 'app/index.html')


def submit_text(request):

    xml = request.POST['pom-code']

    if xml is not None:
        project = process_pom_file(xml)
        request.session['project'] = project
    else:
        if not request.session.__contains__('project'):
            return render(request, 'app/index.html')
        project = request.session['project']

    return render_project(request, project)


def submit_file(request):

    pom_file = request.FILES.get('pom-file')

    if pom_file is not None:
        xml = pom_file.read()
        project = process_pom_file(xml)
        request.session['project'] = project
    else:
        if not request.session.__contains__('project'):
            return render(request, 'app/index.html')
        project = request.session['project']

    return render_project(request, project)


def submit_email(request):

    developer_email = request.POST['email']

    # TODO
    if not EMAIL_REGEX.match(developer_email):
        print "invalid email!"
    else:
        print "valid email!"

    verification_code = uuid.uuid4().__str__()
    verification_code = verification_code.replace('-', '')

    stored_developer = Developer.objects.filter(email=developer_email)
    if stored_developer:
        print "TODO already stored developer"
    else:
        developer = Developer(email=developer_email,
                              email_verification_code=verification_code,
                              email_verification_timestamp=datetime.utcnow(),
                              email_verified=False,
                              send_emails=True)
        developer.save()
        send_verification_email(developer_email, verification_code)

    return render(request, 'app/email-verification-pending.html')


def render_project(request, project):
    dependencies_total_count = len(project.dependencies)
    dependencies_out_of_date = sum(dependency.up_to_date is False for dependency in project.dependencies)
    return render(request, 'app/result.html', {'project_name': project.group_id + ' : ' + project.artifact_id,
                                               'dependencies': project.dependencies,
                                               'dependencies_total_count': dependencies_total_count,
                                               'dependencies_out_of_date': dependencies_out_of_date
                                              })
