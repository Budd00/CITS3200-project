from django.http import HttpResponse

from .models import membership, member_exception

def mod_memdb(request):
    test_mod = membership(member_name = "Admin")
    test_mod.save()
    return HttpResponse("<p>data added!</p>")

def get_membership_data(request):
    response1 = ""
    list = membership.objects.all() #select all
    response2 = membership.objects.filter(id=1)
    for var in list:
        response1 += var.member_name + " "
    return HttpResponse("<p>" + response1 + "</p>")

def del_membership_data(request):
    membership.objects.all().delete()
    return HttpResponse("<p>all data deleted!</p>")