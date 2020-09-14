from .forms import AssetItem,AssetForm, TagForm, LinkForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import check_asset, check_tag, find_assets_direct, check_tag_alternates, add_asset, add_tag, link_asset, link_tags, Asset, find_asset_tags

# library database page
def index(request):
    query = request.GET.get('q')
    option = request.GET.get('option')
    asset_dict = {}
    context = {
        'asset_dict':asset_dict
    }

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
                    tags = find_asset_tags(asset)
                    asset_dict[asset.name] = tags
                return render(request, "libapp/library.html", context)
            #if no related assets found
            else:
                context['error_msg'] = "Tag found but not tied to any assets"
                return render(request, "libapp/library.html", context)
        #logic goes here if tag not found
        else:
            context['error_msg'] = "Tag not found"
            return render(request, "libapp/library.html", context)

    #if the 'asset' radio button was selected
    elif option == 'asset':
        asset = check_asset(query)
        #asset found
        if asset is not None:
            #find related tags
            tags = find_asset_tags(asset)
            asset_dict[asset] = tags
            return render(request, "libapp/library.html", context)
        #no such asset found
        else:
            context['error_msg'] = "No assets found"
            return render(request, "libapp/library.html", context)
    else:
        #retrieves all assets
        asset_list = Asset.objects.all()
        #populates asset_dict in format {asset_1:[tag_1,tag_2],asset_2:[tag_1,tag_4],asset_3...}
        for asset in asset_list:
            tags = find_asset_tags(asset)
            asset_dict[asset] = tags
        context = {
            'asset_dict':asset_dict
        }
        return render(request, "libapp/library.html", context)

#page for asset creation
def asset_create(request):
    if request.method == 'POST':
        form = AssetItem(request.POST)
        if form.is_valid():
            asset_name = form.cleaned_data['name']
            public_notes = form.cleaned_data['public_notes']
            private_notes = form.cleaned_data['private_notes']
            tags = form.cleaned_data['tags']
            new_asset = add_asset(asset_name, public_notes, private_notes)
            if new_asset == None:
                return render(request, 'libapp/fail.html', {'error':'Asset already exists'})
            #If tags were selected
            if tags.exists():
                for tag in tags:
                    link_asset(new_asset, tag, 0)

            return HttpResponseRedirect('/library/')
    else:
        form = AssetItem()

    return render(request, 'libapp/asset-create.html', {'form': form})

#page for asset editing. 
#Navigation to asset editing page occurs when user clicks on any one of the assets at the library homepage
#The editing page for that particular asset shows up as a result
def asset_edit(request):
    asset_name = request.GET.get('asset')
    asset = check_asset(asset_name)
    context = {}
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset.name = form.cleaned_data['name']
            asset.pub_notes = form.cleaned_data['pub_notes']
            asset.priv_notes = form.cleaned_data['priv_notes']
            asset.save()
            return HttpResponseRedirect('/library/')
    else:
        tags = find_asset_tags(asset)
        form = AssetForm(instance=asset)
        context['form'] = form
        return render(request, 'libapp/asset-edit.html', context)

#page for tag creation
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            parent_tags = form.cleaned_data['parent_tags']
            child_tags = form.cleaned_data['child_tags']
            new_tag = add_tag(tag_name)
            if new_tag == None:
                return render(request, 'libapp/fail.html', {'error':'Tag already exists'})
            
            if parent_tags.exists():
                for ptag in parent_tags:
                    link_tags(ptag, new_tag)
            if child_tags.exists():
                for ctag in child_tags:
                    link_tags(new_tag, ctag)
            return HttpResponseRedirect('/library/')
    else:
        form = TagForm()
    
    return render(request, 'libapp/tag-create.html', {'form': form})

def tag_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            parent_tag = form.cleaned_data['parent_tag']
            child_tag = form.cleaned_data['child_tag']
            new_edge = link_tags(parent_tag, child_tag)
            if new_edge == None:
                return render(request, 'libapp/fail.html', {'error':'Link already exists'})
            return HttpResponseRedirect('/library/')
    else:
        form = LinkForm()

    return render(request, 'libapp/tag-link.html', {'form': form})

