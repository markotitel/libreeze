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
    dependencies = check_versions(xml)
    return render(request, 'app/result.html', {'dependencies': dependencies})