from django.shortcuts import render
from app.controller import check_versions

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def submit_text(request):
    xml = request.POST['code']
    dependencies = check_versions(xml)
    return render(request, 'app/result.html', {'dependencies': dependencies})

def submit_file(request):
    item = request.FILES.get('upload')
    print item
    return render(request, 'app/result.html', { 'item': item})
