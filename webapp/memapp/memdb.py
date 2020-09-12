from django.http import HttpResponse

from .models import member_info, member_details

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
    response2 = member_info.objects.filter(id=1)
    for var in list:
        response1 += var.member_name + " "
    return HttpResponse("<p>" + response1 + "</p>")

def del_membership_data(request):
    member_info.objects.all().delete()
    return HttpResponse("<p>all data deleted!</p>")