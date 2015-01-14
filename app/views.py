from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def submit_text(request):
    item = request.body
    return render(request, 'app/result.html', {'item': item})

def submit_file(request):
    item = request.FILES.get('upload')
    return render(request, 'app/result.html', { 'item': item})
