from .forms import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
import urllib.parse

#redirect to library database page if URL is just '/'
def main_index(request):
    return HttpResponseRedirect('/library/')

# view for library database page '/library'
def index(request):
    query = request.GET.get('q')
    option = request.GET.get('option')

    asset_dict = {}
    if option == None:
        option = ''
    context = {
        'asset_dict':asset_dict,
        'option' : option
    }


    #if the 'tag' radio button was selected
    if option == 'tag':
        #split lst into seperate queries
        qList = query.split(", ")
        asset_list = []

        for reqTag in qList:
            #set search type to default (broaden search)
            search_type = 0
            #check if the query includes any specific search modifiers
            if reqTag[:1] == "|":
                #set search type to 1 (refine search)
                search_type = 1
                #remove the search type modifier
                reqTag = reqTag[2:]
            elif reqTag[:1] == "!":
                #det search type to 2 (exclude search)
                search_type = 2
                #remove the search type modifier
                reqTag = reqTag[2:]
            
            #checks if tag exists
            tag = check_tag(reqTag)
            #if tag not found, check if tag is an alternate name
            if tag is None:
                tag = check_tag_alternates(reqTag)
             #if tag is found, find related assets
            if tag is not None:
                #run the search based on what search type was set
                if search_type == 0:
                    asset_list = broaden_asset_search(asset_list, tag)
                elif search_type == 1:
                    asset_list = refine_asset_search(asset_list, tag)
                elif search_type == 2:
                    asset_list = exclude_from_search(asset_list, tag)
            #logic goes here if tag not found
            else:
                context['error_msg'] = "Tag not found"
                return render(request, "libapp/library.html", context)
        #if related assets found
        if asset_list != []:
            #add each asset into asset_list
            for asset in asset_list:
                tags = find_asset_tags_direct(asset)
                asset_dict[asset] = tree(tags, [])
            return render(request, "libapp/library.html", context)
        #if no related assets found
        else:
            context['error_msg'] = "Tag found but not tied to any assets"
            return render(request, "libapp/library.html", context)

    #if the 'asset' radio button was selected
    elif option == 'asset':
        asset_list = fuzzy_check_asset(query)
        #asset found
        if asset_list is not None:
            #find related tags
            for asset in asset_list:
                tags = find_asset_tags_direct(asset)
                asset_dict[asset] = tree(tags, [])
            return render(request, "libapp/library.html", context)
        #no such asset found
        else:
            context['error_msg'] = "No assets found"
            return render(request, "libapp/library.html", context)
    #initial loading of page
    else:
        #retrieves all assets
        asset_list = Asset.objects.all()
        hierarchy = []
        for asset in asset_list:
            tags = find_asset_tags_direct(asset)
            # if tags is not empty
            asset_dict[asset] = tree(tags, [])
        return render(request, "libapp/library.html", context)


@login_required
def asset_delete(request):
    asset_name = request.GET.get('asset')
    asset = check_asset(asset_name)
    tags = find_asset_tags_direct(asset)
    for tag in tags:
        remove_asset_edge(asset, tag)
    asset.delete()
    return HttpResponseRedirect('/library/')

@login_required
#remove an alternate name    
def alt_delete(request):
    alt_name = request.GET.get('alt')
    tag = check_tag_alternates(alt_name)
    if tag is not None:
        alt = AlternateName.objects.filter(name__iexact=alt_name)
        alt.delete()
    return HttpResponseRedirect('/library/')

#recursive function for printing out the tag hierarchy
def tree(tags, hierarchy):
    if tags:
        if hierarchy:
            hierarchy.append("indent")
        for tag in tags:
            hierarchy.append(tag)
            hierarchy = tree(tag.child(), hierarchy)
        hierarchy.append("dedent")
        return hierarchy
    else:
        return hierarchy

@login_required
#page for asset creation
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset_name = form.cleaned_data['name']
            public_notes = form.cleaned_data['pub_notes']
            private_notes = form.cleaned_data['priv_notes']
            tags = form.cleaned_data['tags']
            new_asset = add_asset(asset_name, public_notes, private_notes)
            if new_asset == None:
                return render(request, 'libapp/asset-create.html', {'form': form, 'error':'Asset name unavailable. Please enter another name.'})
            #If tags were selected
            if tags.exists():
                for tag in tags:
                    link_asset(new_asset, tag, 0)
                    new_asset.tags.add(tag)

            return HttpResponseRedirect('/library/')
    else:
        form = AssetForm()

    return render(request, 'libapp/asset-create.html', {'form': form})

@login_required
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
            #if not none, asset name is taken
            if check_asset(form.cleaned_data['name']) != None and form.cleaned_data['name'] != asset.name:
                form = AssetForm(instance=asset)
                asset_tags = find_asset_tags_direct(asset)
                context['form'] = form
                context['asset_tags'] = asset_tags
                context['error'] = 'Asset name unavailable. Please enter another name.'
                return render(request, 'libapp/asset-edit.html', context)
            asset.name = form.cleaned_data['name']
            asset.pub_notes = form.cleaned_data['pub_notes']
            asset.priv_notes = form.cleaned_data['priv_notes']
            tags = form.cleaned_data['tags']
            if tags.exists():
                asset.tags.clear()
                linked_tags = find_asset_tags_direct(asset)
                for tag in linked_tags:
                    remove_asset_edge(asset, tag)
                for tag in tags:
                    link_asset(asset, tag, 0)
                    asset.tags.add(tag)
            else:
                asset.tags.clear()
                linked_tags = find_asset_tags_direct(asset)
                for tag in linked_tags:
                    remove_asset_edge(asset, tag)                
            asset.save()
            
            return HttpResponseRedirect('/library/')
    else:
        form = AssetForm(instance=asset)
        asset_tags = find_asset_tags_direct(asset)
        context['form'] = form
        context['asset_tags'] = asset_tags
        return render(request, 'libapp/asset-edit.html', context)

@login_required
#page for tag editing.
#Navigation to tag editing page occurs when user clicks on any one of the tags in the tag linking page
#The editing page for that particular tag shows up as a result
def tag_edit(request):
    tag_name = request.GET.get('tag')
    tag = check_tag(tag_name)
    tag_list = Tag.objects.all()
    context = {}
    if request.method == 'POST':
        form = TagEditForm(request.POST)
        if form.is_valid():
            
            new_name = form.cleaned_data['name']
            if new_name != "" and new_name != " ":
                tag.name = new_name
            alt_names = form.cleaned_data['new_alts']
            
            if alt_names != "" and alt_names != " ":
                alternate_names = alt_names.split(", ")
                for name in alternate_names:
                    add_alternate_name(tag, name)

            tag.save()

            return HttpResponseRedirect('/library/tag-link/')
    else:
        form = TagEditForm()
        current_alts = find_alternate_name(tag)
        context['alts'] = current_alts
        if current_alts is not None:
            context['altlen'] = len(current_alts)
        else:
            context['altlen'] = 0
        context['tag'] = tag
        context['form'] = form
        context['tag_list'] = tag_list
        return render(request, 'libapp/tag-edit.html', context)

@login_required
#page for tag creation
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            alt_names = form.cleaned_data['alt_names']
            alternate_names = alt_names.split(", ")
            parent_tags = form.cleaned_data['parent_tags']
            new_tag = add_tag(tag_name)
            if new_tag == None:
                return render(request, 'libapp/fail.html', {'error':'Tag already exists'})
            
            for name in alternate_names:
                add_alternate_name(new_tag, name)

            if parent_tags.exists():
                for ptag in parent_tags:
                    link_tags(ptag, new_tag)
                
            
            return HttpResponseRedirect('/library/tag-link')
    else:
        form = TagForm()

    return render(request, 'libapp/tag-create.html', {'form': form})

@login_required
#page for tag linking
def tag_link(request):
    tags = Tag.objects.all()
    tag_urls = {}
    for tag in tags:
        url_name = urllib.parse.quote(tag.name)
        tag_urls[tag.name] = url_name
    return render(request, 'libapp/tag-link.html', {'tags':tags, 'urls':tag_urls})

@login_required
#function for unlinking the currently selected tag from the selected parent
def tag_unlink(request):
    parent_tag = check_tag_id(request.POST.get('parent_tag'))
    current_tag = check_tag_id(request.POST.get('current_tag'))
    root_tag = check_tag_id(request.POST.get('root_tag'))
    remove_edge(parent_tag, current_tag)
    return HttpResponseRedirect('/library/tag-link/tag-edit-connections/?tag=' + root_tag.name)

@login_required
#function for adding a new child tag to the currently selected tag
def tag_add_child(request):
    child_tag = check_tag_id(request.POST.get('child_tag'))
    current_tag = check_tag_id(request.POST.get('current_tag'))
    root_tag = check_tag_id(request.POST.get('root_tag'))
    link_tags(current_tag, child_tag)
    #temp fixve
    if root_tag == None:
        root_tag = current_tag
    
    return HttpResponseRedirect('/library/tag-link/tag-edit-connections/?tag=' + root_tag.name)

#view for editing tag connections
def tag_edit_connections(request):
    tag_list = Tag.objects.all()
    tag_name = request.GET.get('tag')
    current_tag = check_tag(tag_name)
    return render(request, 'libapp/tag-edit-connections.html', {'tag_list':tag_list, 'current_tag': current_tag})

#function for deleting a tag
def tag_delete(request):
    current_tag = check_tag_id(request.POST.get('current_tag'))
    current_tag.delete()
    return HttpResponseRedirect('/library/tag-link')