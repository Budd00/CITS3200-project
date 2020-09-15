from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from . import models
from .models import member_info, member_details
from django.views import generic
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

def del_membership_data(request):
    member_info.objects.all().delete()
    return HttpResponse("<p>all data deleted!</p>")