from django.shortcuts import render
from django.http import HttpResponse
from .models import check_asset, check_tag, find_assets_direct, check_tag_alternates

# Create your views here.
def index(request):
    #return HttpResponse("Library Management Home Page :)")
    return render(request, "libapp/search.html")

#search result view
def search_result(request):
    result_list = []
    context = {
        'result_list':result_list
    }
    query = request.GET.get('q')
    option = request.GET.get('option')

    #if the 'tag' radio button was selected
    if option == 'tag':
        #checks if tag exists
        tag = check_tag(query)
        #if tag not found, check if tag is an alternate name
        if tag is None:
            tag = check_tag_alternates(query)

        #if tag is found, find related assets
        if tag is not None:
            
            asset_list = find_assets_direct(tag)
            #if related assets found
            if asset_list != []:
                #add each asset into asset_list
                for asset in asset_list:
                    result_list.append(asset.name)
                return render(request, "libapp/search-result.html", context)
            #if no related assets found
            else:
                result_list.append('Tag found but is not tied to any assets')
                return render(request, "libapp/search-result.html", context)
        #logic goes here if tag not found
        else:
            result_list.append('Tag not found')
            return render(request, "libapp/search-result.html", context)

    #if the 'asset' radio button was selected
    elif option == 'asset':
        asset = check_asset(query)
        if asset is not None:
            result_list.append(asset.name)
            return render(request, "libapp/search-result.html", context)
        else:
            result_list.append('No assets found')
            return render(request, "libapp/search-result.html", context)
