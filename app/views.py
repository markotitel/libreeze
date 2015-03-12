from django.shortcuts import render
from app.controller import check_versions

# Create your views here.


def index(request):
    # TODO move to static
    return render(request, 'app/index.html')


def submit_text(request):
    xml = request.POST['pom-code']
    return parse_and_render(request, xml)


def submit_file(request):
    file = request.FILES.get('pom-file')
    # TODO check file size first and check that the file is actually uploaded
    xml = file.read()
    return parse_and_render(request, xml)

def parse_and_render(request, xml):
    project = check_versions(xml)
    dependencies_total_count = len(project.dependencies)
    dependencies_out_of_date = sum(dependency.up_to_date is False for dependency in project.dependencies)
    return render(request, 'app/result.html', {'dependencies': project.dependencies,
                                               'dependencies_total_count': dependencies_total_count,
                                               'dependencies_out_of_date': dependencies_out_of_date
                                              })
