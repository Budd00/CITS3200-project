from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("Member Management Home Page :)")
