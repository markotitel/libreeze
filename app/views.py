import uuid
import re
import logging

from datetime import datetime

from django.shortcuts import render

from app.controller import process_pom_file
from app.models import Developer, MavenProjectDependency, MavenProject, MavenRepoDependency
from app.mail import send_verification_email

# Get an instance of a logger
logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Create your views here.


def index(request):
    # TODO move to static
    return render(request, 'app/index.html')


def submit_text(request):

    xml = request.POST['pom-code']

    if xml is not None:
        try:
            project = process_pom_file(xml)
            request.session['project'] = project
        except Exception as e:
            logger.exception("Invalid xml supplied!", e)
            return render(request, 'app/index.html', {'error': 'Supplied xml is not a valid pom file.'})
    else:
        if not request.session.__contains__('project'):
            return render(request, 'app/index.html')
        project = request.session['project']

    return render_project(request, project)


def submit_file(request):

    pom_file = request.FILES.get('pom-file')

    if pom_file is not None:
        xml = pom_file.read()
        try:
            project = process_pom_file(xml)
            request.session['project'] = project
        except Exception as e:
            print("Invalid pom file supplied!")
            logger.exception("Invalid pom file!", e)
            return render(request, 'app/index.html', {'error': 'Supplied file is not a valid pom file.'})
    else:
        if not request.session.__contains__('project'):
            return render(request, 'app/index.html')
        project = request.session['project']

    return render_project(request, project)


def submit_email(request):

    developer_email = request.POST['email']

    # TODO handle session expiry
    if not request.session.__contains__('project'):
        return render(request, 'app/index.html')

    project = request.session['project']

    if not EMAIL_REGEX.match(developer_email):
        return render_project(request, project, 'Supplied email is not a valid email address.')

    verification_code = uuid.uuid4().__str__()
    verification_code = verification_code.replace('-', '')

    stored_developer = Developer.objects.filter(email=developer_email)

    # Existing dev, verified email
    if stored_developer.exists():
        developer = stored_developer[0]
        if developer.email_verified:
            context = {'verified_email': developer_email}
        else:
            # existing dev, email not verified yet
            developer.verification_code = verification_code
            developer.email_verification_timestamp=datetime.utcnow()
            developer.save()
            send_verification_email(developer_email, verification_code)
            context = {'unverified_email': developer_email}

    else:
        # new developer
        developer = Developer(email=developer_email,
                              email_verification_code=verification_code,
                              email_verification_timestamp=datetime.utcnow(),
                              email_verified=False,
                              send_emails=True)
        developer.save()
        send_verification_email(developer_email, verification_code)
        context = {'unverified_email': developer_email}

    # Create developer specific project
    stored_projects = MavenProject.objects.filter(developer=developer, group_id=project.group_id, artifact_id=project.artifact_id)

    if stored_projects.exists():
        # project already stored, remove existing dependencies
        stored_project = stored_projects[0]
        stored_project.send_updates=True
        stored_project.save()
        MavenProjectDependency.objects.filter(project=stored_project).delete()
        maven_project = stored_project
    else:
        unsubscribe_code = uuid.uuid4().__str__()
        unsubscribe_code = unsubscribe_code.replace('-', '')
        maven_project = MavenProject(developer=developer,
                                     group_id=project.group_id,
                                     artifact_id=project.artifact_id,
                                     version=project.version,
                                     send_updates=True,
                                     unsubscribe_code=unsubscribe_code)
        maven_project.save()

    # Mark its dependencies
    for dto in project.dependencies:
        repo_dependencies= MavenRepoDependency.objects.filter(group_id=dto.group_id, artifact_id=dto.artifact_id)
        if repo_dependencies.exists():
            repo_dependency = repo_dependencies[0]
        else:
            repo_dependency = None
        project_dependency = MavenProjectDependency(project=maven_project,
                                                    repo_dependency=repo_dependency,
                                                    group_id=dto.group_id,
                                                    artifact_id=dto.artifact_id,
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
            context = {'verified_email': developer.email}
            return render(request, 'app/email-verification.html', context)

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
