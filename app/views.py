import uuid
import re
import logging
import traceback

from datetime import datetime

from django.shortcuts import render

from app.controller import process_pom_file
from app.models import Developer, ProjectDependency, Project, RepoDependency
from app.mail import send_verification_email

# Get an instance of a logger
logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Create your views here.


def index(request):

    return render(request, 'app/index.html')


def submit_text(request):

    xml = request.POST['pom-code']

    if xml is not None:
        try:
            logger.debug("Received xml as text: %s" % xml)
            project = process_pom_file(xml)
            request.session['project'] = project
        except Exception as e:
            logger.exception("Invalid xml supplied!")
            return render(request, 'app/index.html', {'error': 'Supplied xml is not a valid pom file.'})
    else:
        if not request.session.__contains__('project'):
            logger.error("No project found in session, returning index page!")
            return render(request, 'app/index.html')
        project = request.session['project']

    return render_project(request, project)


def submit_file(request):

    pom_file = request.FILES.get('pom-file')

    if pom_file is not None:
        xml = pom_file.read()
        try:
            logger.debug("Received xml as file: %s" % xml)
            project = process_pom_file(xml)
            request.session['project'] = project
        except Exception as e:
            logger.exception("Invalid pom file!")
            return render(request, 'app/index.html', {'error': 'Supplied file is not a valid pom file.'})
    else:
        if not request.session.__contains__('project'):
            logger.error("No project found in session, returning index page!")
            return render(request, 'app/index.html')
        project = request.session['project']

    return render_project(request, project)


def submit_email(request):

    developer_email = request.POST['email']

    # TODO handle session expiry
    if not request.session.__contains__('project'):
        logger.error("No project found in session, returning index page!")
        return render(request, 'app/index.html')

    project = request.session['project']

    if not EMAIL_REGEX.match(developer_email):
        logger.debug("Invalid email %s received" % developer_email)
        return render_project(request, project, 'Supplied email is not a valid email address.')

    logger.debug("Received email %s" % developer_email)

    verification_code = create_unique_code()

    stored_developer = Developer.objects.filter(email=developer_email)

    # Existing dev, verified email
    if stored_developer.exists():
        developer = stored_developer[0]
        logger.debug("Developer already known: %s" % developer)
        if developer.email_verified:
            logger.debug("Developer's mail already verified, proceeding...")
            context = {'verified_email': developer_email}
        else:
            # existing dev, email not verified yet
            logger.debug("Developer's mail not yet verified, recreating the code...")
            developer.email_verification_code = verification_code
            developer.email_verification_timestamp = datetime.utcnow()
            developer.save()
            send_verification_email(developer_email, verification_code)
            context = {'unverified_email': developer_email}

    else:
        # new developer
        logger.debug("New developer, creating a db entry...")
        developer = Developer(email=developer_email,
                              email_verification_code=verification_code,
                              email_verification_timestamp=datetime.utcnow(),
                              email_verified=False,
                              send_emails=True,
                              unsubscribe_code=create_unique_code())
        developer.save()
        send_verification_email(developer_email, verification_code)
        context = {'unverified_email': developer_email}

    # Create developer specific project
    stored_projects = Project.objects.filter(developer=developer, namespace=project.group_id, name=project.artifact_id)

    if stored_projects.exists():
        stored_project = stored_projects[0]
        logger.debug("Project %s already stored, resetting dependencies..." % stored_project)
        stored_project.send_updates=True
        stored_project.save()
        ProjectDependency.objects.filter(project=stored_project).delete()
        maven_project = stored_project
    else:
        maven_project = Project(developer=developer,
                                namespace=project.group_id,
                                name=project.artifact_id,
                                version=project.version,
                                send_updates=True,
                                unsubscribe_code=create_unique_code())
        logger.debug("New project %s, creating a db entry..." % maven_project)
        maven_project.save()

    # Mark its dependencies
    for dto in project.dependencies:
        repo_dependencies= RepoDependency.objects.filter(namespace=dto.group_id, name=dto.artifact_id)
        if repo_dependencies.exists():
            repo_dependency = repo_dependencies[0]
        else:
            repo_dependency = None
        project_dependency = ProjectDependency(project=maven_project,
                                               repo_dependency=repo_dependency,
                                               namespace=dto.group_id,
                                               name=dto.artifact_id,
                                               version=dto.version)
        project_dependency.save()

    return render(request, 'app/email-verification.html', context)


def verify_email(request):

    code = request.GET['code']

    if code is not None:
        developers = Developer.objects.filter(email_verification_code=code)
        if developers.exists():
            developer = developers[0]
            developer.email_verified=True
            developer.save()
            logger.debug("Email %s verified!" % developer.email)
            context = {'verified_email': developer.email}
            return render(request, 'app/email-verification.html', context)
        else:
            logger.error("Unrecognized verification code %s received!" % code)

    return render(request, 'app/index.html')


def render_project(request, project, error=None):
    dependencies_total_count = len(project.dependencies)
    dependencies_out_of_date = sum(dependency.up_to_date is False for dependency in project.dependencies)
    context = {'project_name': project.group_id + ' : ' + project.artifact_id,
               'dependencies': project.dependencies,
               'dependencies_total_count': dependencies_total_count,
               'dependencies_out_of_date': dependencies_out_of_date}
    if error is not None:
        context['error'] = error
    return render(request, 'app/result.html', context)


def unsubscribe(request):

    code = request.GET['code']

    if code is not None:
        developers = Developer.objects.filter(email_verification_code=code)
        if developers.exists():
            developer = developers[0]
            developer.send_emails=False
            developer.save()
            logger.warn("Developer %s unsubscribed!" % developer.email)
            return render(request, 'app/unsubscribe.html')
        else:
            logger.error("Unrecognized unsubscribe code %s received!" % code)

    return render(request, 'app/index.html')


def unsubscribe_project(request):

    code = request.GET['code']

    if code is not None:
        projects = Project.objects.filter(unsubscribe_code=code)
        if projects.exists():
            project = projects[0]
            project.send_updates=False
            project.save()
            context = {'project_name': project.group_id + ' : ' + project.artifact_id}
            logger.warn("Project %s unsubscribed!" % project)
            return render(request, 'app/unsubscribe_project.html', context)
        else:
            logger.error("Unrecognized unsubscribe project code %s received!" % code)

    return render(request, 'app/index.html')


def create_unique_code():
    code = uuid.uuid4().__str__()
    return code.replace('-', '')


def support(request):
    return render(request, 'app/support.html')


def faq(request):
    return render(request, 'app/faq.html')


# --- GUI testing purpose methods

def devtest_verify_email(request):
    context = {'verified_email': "test@acme.com"}
    return render(request, 'app/email-verification.html', context)


def devtest_unsubscribe(request):
    return render(request, 'app/unsubscribe.html')


def devtest_unsubscribe_project(request):
    context = {'project_name': 'com.wolkabout.m2m : server'}
    return render(request, 'app/unsubscribe_project.html', context)

# --- end of GUI testing purpose methods
