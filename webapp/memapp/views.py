from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from . import models
from .models import member_info, member_details
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'members'

    def get_queryset(self):
        return member_info.objects.order_by('id')


class DetailView(generic.DetailView):
    model = member_info
    template_name = "member_info.html"


def add_detail(request):
    info_obj = models.member_info.objects.filter(pk = 1).first()
    detail = models.member_details.objects.create(id = info_obj,
                                email = "21890522@student.uwa.edu.au",
                                phone_num = 415133276,)
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


def get_membership_data(request,m_id):
    result = member_info.objects.get(id = m_id)
    return HttpResponse("<p>" + str(result) + "</p>")

# get detail data using member id
def get_detail_data(request, m_id):
    try:
        list = ""
        result = member_info.objects.get(id = m_id).member_details_set.all()
        for st in result:
            list += str(st)
    except member_info.DoesNotExist:
        raise Http404("Detail does not exist.")
    return HttpResponse("<p>" + list + "</p>")

def create_user(request):
    # Create user and save to the database
    user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

    # Update fields and then save again
    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()
    return HttpResponse("<p> user created! </p>")

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request,username=username, password = password)
    if user is not None:
        login(request, user)
    else:
        return Http404("User does not exist")

@login_required(login_url='/member/login')
def logout_view(request):
    logout(request)