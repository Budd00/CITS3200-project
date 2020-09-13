from .forms import AssetForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import check_asset, check_tag, find_assets_direct, check_tag_alternates, add_asset, link_asset, Asset, find_asset_tags

# library database page
def index(request):
    #return HttpResponse("Library Management Home Page :)")
    asset_list = Asset.objects.all()
    asset_dict = {}
    for asset in asset_list:
        tags = find_asset_tags(asset)
        asset_dict[asset.name] = tags
    context = {
        'asset_dict':asset_dict
    }
    return render(request, "libapp/library.html", context)

#search page
def search(request):
    return render(request, "libapp/search.html")

#page for asset creation
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset_name = form.cleaned_data['name']
            public_notes = form.cleaned_data['public_notes']
            private_notes = form.cleaned_data['private_notes']
            tags = form.cleaned_data['tags']
            new_asset = add_asset(asset_name, public_notes, private_notes)
            #If tags were selected
            if tags.exists():
                for tag in tags:
                    link_asset(new_asset, tag, 0)

            return HttpResponseRedirect('/library/')
    else:
        form = AssetForm()

    
    return render(request, 'libapp/asset-create.html', {'form': form})

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
