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

def mod_memdb(request):
    test_mod = member_info(member_name = "Xinhao",
                           dob = "1999-05-27",
                           is_committee = True,
                           join_date = "2020-09-11")
    test_mod.save()
    return HttpResponse("<p>data added!</p>")
def mod_memdetail(request):
    test_mod = member_details(id = 1,
                                email = "21890522@student.uwa.edu.au",
                                phone_num = 415133276,
    )
    test_mod.save()
    return HttpResponse("<p>data added!</p>")
def get_membership_data(request):
    response1 = ""
    list = member_info.objects.all() #select all
    for var in list:
        response1 += var.member_name + " "
    return HttpResponse("<p>" + response1 + "</p>")

def get_detail_data(request):
    response = ""
    list = member_details.objects.all()
    for var in list:
        response += str(var.id) + " "
    return HttpResponse("<p>" + response + "</p>")

def del_membership_data(request):
    member_info.objects.all().delete()
    return HttpResponse("<p>all data deleted!</p>")