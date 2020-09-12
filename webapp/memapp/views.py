from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .models import member_info, member_details

# Create your views here.

def hello(request):
    return HttpResponse("Hello world!")

def add_detail(request):
    info_obj = models.member_info.objects.filter(pk = 1).first()
    detail = models.member_details.objects.create(id = info_obj,
                                email = "21890522@student.uwa.edu.au",
                                phone_num = 415133276,)
    print(info_obj,detail )
    return HttpResponse("detail added!")
