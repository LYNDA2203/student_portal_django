from django.shortcuts import HttpResponse

# Create your views here.
def course(request):
    return HttpResponse('<h1>Select the courses<\h1>')
