from django.shortcuts import render
from app.controller import process_pom_file

# Create your views here.


def index(request):
    # TODO move to static
    return render(request, 'app/index.html')


def submit_text(request):
    xml = request.POST['pom-code']
    project = process_pom_file(xml)
    request.session['project'] = project
    return parse_and_render(request, project)


def submit_file(request):

    pom_file = request.FILES.get('pom-file')

    if pom_file is not None:
        xml = pom_file.read()
        project = process_pom_file(xml)
        request.session['project'] = project
    else:
        # This handles refresh without submit on result page
        project = request.session['project']

    # TODO handle when project is not in the session

    return parse_and_render(request, project)


def submit_email(request):
    return render(request, 'app/email.html')


def parse_and_render(request, project):
    dependencies_total_count = len(project.dependencies)
    dependencies_out_of_date = sum(dependency.up_to_date is False for dependency in project.dependencies)
    return render(request, 'app/result.html', {'project_name': project.group_id + ' : ' + project.artifact_id,
                                               'dependencies': project.dependencies,
                                               'dependencies_total_count': dependencies_total_count,
                                               'dependencies_out_of_date': dependencies_out_of_date
                                              })
