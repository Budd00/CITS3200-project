from django.db import models
import uuid

# Create your models here.
#create asset table
#!!!---Placeholder---!!!
class Asset(models.Model):
    
    #primary key
    id = models.UUIDField(default=uuid.uuid4, primary_key = True)
    #name
    name = models.CharField(max_length = 64)
    #Any notes for the public to read. ie. description
    pub_notes = models.TextField(blank=True)
    #Any notes not for the public to read. ie. missing peices, maintenance issues
    priv_notes = models.TextField(blank=True)

    #return this asset name
    def __repr__(self):
        return self.name

#Create tag table
class Tag(models.Model):

    #Initialise attributes
    #primary key
    id          = models.UUIDField(default=uuid.uuid4, primary_key = True)
    #tag name
    name        = models.CharField(max_length=64)
    #Number of times searched
    popularity  = models.IntegerField(default=0)

    #return this tag name
    def __repr__(self):
        return self.name

    #increase the popularity
    def increase_pop(self):
        self.popularity += 1

#Create tag edges table to track the connections in the graph
class Edge(models.Model):

    #initilise attributes
    #primary key
    id          = models.UUIDField(default=uuid.uuid4, primary_key = True)
    #tag id of the parent tag
    parent_tag  = models.ForeignKey(Tag,related_name='%(class)s_parent', on_delete=models.CASCADE,default=uuid.uuid4)
    #tag id of the child tag
    child_tag   = models.ForeignKey(Tag,related_name='%(class)s_child', on_delete=models.CASCADE,default=uuid.uuid4)

    #return this edge id
    def __repr__(self):
        return str(self.id)

#Create Asset to tag edges table to track asset tags
class AssetEdge(models.Model):

    #initialise attributes
    #primary key
    id          = models.UUIDField(default=uuid.uuid4, primary_key = True)
    #id of the asset
    asset_id    = models.ForeignKey(Asset, on_delete=models.CASCADE)
    #id of linked tag

    tag_id      = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #determines whether the link is an implied or direct edge
    #0 - direct link, 1- implied link
    implied     = models.IntegerField(default=0)

    
    #return this edge id
    #__repr__ returns TypeError when trying to return type UUID. Str() is used to combat this
    def __repr__(self):
        return str(self.id)

#Create AlternateName table for tags which are known by multiple terms
class AlternateName(models.Model):

    #primary key
    id          = models.UUIDField(default=uuid.uuid4, primary_key = True)
    #Tag ID
    tag_id      = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #Alternate name of tag
    name        = models.CharField(max_length = 64)

    #return the alternate name
    def __repr__(self):
        return self.name

#check if the tag exists, if it doesn't, create one. returns the found/created tag
def add_tag(name):
    #search for a tag with the given name
    if check_tag(name) == None:
        new_tag = Tag.objects.create(name=name)
        return new_tag
    return None

#check if the asset exists, if it doesn't, create one. returns the found/created asset
def add_asset(name, public_notes, private_notes):
    if check_asset(name) == None:
        new_asset = Asset.objects.create(name=name, pub_notes = public_notes, priv_notes = private_notes)
        return new_asset
    return None

#Given two tags, create an edge link from parent to child
def link_tags(parent, child):
    #check that the edge doesn't already exist
    existingEdge = Edge.objects.filter(parent_tag__exact = parent.id).filter(child_tag__exact = child.id)
    if len(existingEdge) == 0:
        #if it doesn't exist, create a new edge
        newEdge = Edge.objects.create(parent_tag = parent, child_tag = child)
        #check for any new implied links between assets and tags
        implied_assets_new(newEdge)
        return newEdge
    return None

#Given an asset and a tag, link the tag to the asset
def link_asset(asset, tag, implied):
    thisAsset = asset
    thisTag = tag
    print("linking")
    print(thisAsset.name)
    print(thisAsset.id)
    print(thisTag.name)
    #check that there isn't already a link
    #find all edges to the asset
    existingEdges = AssetEdge.objects.filter(asset_id__exact = asset.id)
    #set exists variable to false
    exists = False
    #check each edge to see if the given tag is already linked
    for edge in existingEdges:
        if edge.tag_id == thisTag.id:
            print(edge.asset_id)
            exists = True
    if not exists:
        print("creating")
        newEdge = AssetEdge.objects.create(asset_id = thisAsset, tag_id = thisTag, implied=implied)
        print(newEdge.asset_id)
        return newEdge
        #AssetEdge.objects.create(asset_id = thisAsset, tag_id = thisTag, implied=implied)
        #only check if this is a direct edge
        if implied == 0:
            #check for any new implied links between assets and tags
            implied_assets_from_direct(newEdge)
    return None

#checks if the given tag exists
def check_tag(tag_name):
    tag_query = Tag.objects.filter(name__exact=tag_name)
    #returns the tag if exists
    if tag_query.exists():
        return tag_query[0]
    else:
        return None

#checks if the given asset exists
def check_asset(asset_name):
    asset_query = Asset.objects.filter(name__exact=asset_name)
    #returns the asset if exists
    if asset_query.exists():
        return asset_query[0]
    else:
        return None

#returns a list of assets with direct links to this tag, ignoring any assets in the found list
def find_assets_direct(tag, found=[]):
    #empty list to store found assets
    assets= []
    #find all edges linking an asset to the given tag
    asset_query = AssetEdge.objects.filter(tag_id__exact=tag.id)
    #for each edge found, retrieve the asset
    for link in asset_query:


        this_asset = Asset.objects.filter(id__exact = link.asset_id.id)[0]


        #if the found asset is not in the "found" list, and is a dirent link, add it to the assets list
        if this_asset not in found and (link.implied == 0):
            assets.append(this_asset)
    #return the assets list
    return assets

#returns a list of assets with direct links to this tag, ignoring any assets in the found list
def find_assets(tag, found=[]):
    #empty list to store found assets
    assets= []
    #find all edges linking an asset to the given tag
    asset_query = AssetEdge.objects.filter(tag_id__exact=tag.id)
    #for each edge found, retrieve the asset
    for link in asset_query:
        this_asset = Asset.objects.filter(id__exact = link.asset_id.id)[0]

        #if the found asset is nt in the "found" list, add it to the assets list
        if this_asset not in found:
            assets.append(this_asset)
    #return the assets list
    return assets

#returns a list of tags with direct links to this asset, ignoring any tags in the ignore list
def find_asset_tags_direct(asset, ignore=[]):
    #empty list to store found tags
    tags= []
    #find all edges linking a tag to the given asset
    tag_query = AssetEdge.objects.filter(asset_id__exact=asset.id)
    #for each edge found, retrieve the tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.tag_id)[0]
        #if the found tag is not in the ignore list, and is a direct link, add it to the tags list
        if this_tag not in ignore and (link.implied == 0):
            assets.append(this_tag)
    #return the tags list
    return assets

#returns a list of tags with direct links to this asset, ignoring any tags in the ignore list
def find_asset_tags(asset, ignore=[]):
    #list to store tags that have been found
    found = []
    #empty list to store found tags
    tags= []
    #find all edges linking a tag to the given asset
    tag_query = AssetEdge.objects.filter(asset_id__exact=asset.id)
    #for each edge found, retrieve the tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.tag_id.id)[0]
        #if the found tag is not in the ignore list, add it to the tags list
        if this_tag not in ignore and this_tag not in found:
            tags.append(this_tag)
            found.append(this_tag)
    #return the tags list
    return tags


#returns a list of tags that imply the given tag, ignoring any tags in the ignore list
def find_parent_tags(tag, ignore=[]):
#returns a list of tags that directly imply the given tag, ignoring any tags in the ignore list
    #empty tags list to store found parent tags
    tags = []
    #find all edges with the given tag as the child tag
    tag_query = Edge.objects.filter(child_tag__exact = tag.id)
    #for each edge found, retreive the parent tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.parent_tag.id)[0]
        #if the parent tag is not in the ignore list, add it to the tags list
        if this_tag.id not in ignore:
            tags.append(this_tag)
    #return the tags list
    return tags

    #returns a list of tags that the given tag implies, ignoring any tags in the ignore list
def find_child_tags(tag, ignore=[]):
    #returns a list of tags that the given tag directly implies, ignoring any tags in the ignore list
    #empty tags list to store found child tags
    tags = []
    #find all edges with the given tag as the parent tag
    tag_query = Edge.objects.filter(parent_tag__exact = tag.id)
    #for each edge found, retreive the child tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.child_tag.id)[0]
        #if the child tag is not in the ignore list, add it to the tags list
        if this_tag.id not in ignore:
            tags.append(this_tag)
    #return the tags list
    return tags

#returns a list of all tags that are children of the given tag, directly or implicitly.
#any tags in the ignore list are not checked or added
def reachable_child(start, ignore=[]):
    #create empty list to store tags that have been checked
    checked = []
    #create empty list to store tags that need to be checked (acts as a stacck)
    tags = []
    #add the starting tag to the stack
    tags.append(start)
    #loop over the tags in the stack untill all tags have been exhausted
    while len(tags) >0:
        #remove the next tag in the stack
        checking = tags.pop(len(tags)-1)
        #add the current tag to the list of checked tags
        checked.append(checking)
        #find all tags that share an edge with the current tag, ignoring those already checked and the ignore list
        children = find_child_tags(checking, checked+ignore)
        #add the found children to the stack
        tags = tags+children
    #return the list of children found
    return checked


#returns a list of assets linked to the given tag either directly or implicitly
#def find_all_assets(tag):
    #initialise the empty list of assets
    #assets = []
    #list to store any tags that have been checked to avoid cycles
    #tags_checked = []
    #the list of parent tags that have been found used as a stack
    #tags_to_check = []
    #add the given tag to the list of tags to check
    #tags_to_check.append(tag)
    #cycle over the list of tags to check until there are no more to check
    #while len(tags_to_check) > 0:
        #remove the newest tag from the stack
        #checking = tags_to_check.pop(len(tags_to_check)-1)
        #find all parent tags for the current tag
        #parents = find_parent_tags(checking, tags_checked)
        #add the current tag to the list of checked tags
        #tags_checked.append(checking)
        #add all new parents to the stack to be checked
        #tags_to_check = tags_to_check+parents

        #find all assets directly linked to the current tag
        #these_assets = find_assets_direct(checking, assets)
        #add found assets to the list of assets
        #assets = assets + these_assets
    #return the list of found assets

    #return assets

#returns a list of alternate names for that tag
def find_alternate_name(tag):
    alternate_names = []
    alternate_name_query = AlternateName.objects.filter(tag_id__exact = tag.id)
    for name in alternate_name_query:
        alternate_names.append(name)
    return alternate_names

#checks if the given name is an alternate name. If so, returns the tag id
def check_tag_alternates(name):
    alternate_name_query = AlternateName.objects.filter(name__exact = name)
    if alternate_name_query.exists():
        return alternate_name_query[0].tag_id
    else:
        return None

    #return assets

#finds all assets linked to a parent tag in an edge and links them to all the child tags of that edge
def implied_assets_new(edge):
    print("heya")
    #find the parent tag linked to the edge
    this_parent = Tag.objects.filter(id__exact = edge.parent_tag.id)[0]
    #find the child tag linked to the edge
    this_child =  Tag.objects.filter(id__exact = edge.child_tag.id)[0]
    #find all assets already linked to the parent tag
    assets = find_assets(this_parent)
    #find all tags that are children of the child tag
    children = find_child_tags(this_child)
    #create a link between each asset and each tag found if non already exists
    print(this_parent.name)
    print(this_child.name)
    for asset in assets:
        print(asset.name)
        #add a link to the initial child tag
        link_asset(asset, this_child, 1)
        for tag in children:
            link_asset(asset, tag, 1)
    return

#finds all tags implied by a direct link between an asset and a tag, then creates an implied link between the asset and all the children of that tag
def implied_assets_from_direct(edge):
    #find the parent asset linked to the edge
    this_asset = Asset.objects.filter(id__exact = edge.asset_id)[0]
    #find the child tag linked to the edge
    this_child =  Tag.objects.filter(id__exact = edge.tag_id)[0]
    #find all tags that are children of the child tag
    children = find_child_tags(this_child)
    #create a link between the asset and each tag found if none already exists
    for tag in children:
        link_asset(asset, tag, 1)
    return

#check all assets linked to the given tag to ensure all implied links are still accurate
def clear_false_links(tag):
    #find all assets linked to the given tag
    assets = find_assets(tag)
    #for each asset, remove all implicit links and create new links to every tag that it is now implicitly linked to
    for asset in assets:
        #find all edges to the asset that are implied
        impl_edges = AssetEdge.objects.filter(asset_id__exact = asset.id).filter(implied__exact = 1)
        #delete all implied edges
        for edge in impl_edges:
            edge.delete()
        #find all tags directly linked to the asset
        direct_tags = find_asset_tags_direct(asset)
        #create list to store linkedt tags
        linked = []
        #add direct tags to the list of linked tags
        linked = linked+direct_tags
        #for each direct tag, find all the tags it implies and link them to the asset
        for tag in direct_tags:
            #find all the tags that this tag implies, ignoring tags that have already been linked
            reachable = reachable_child(tag, linked)
            #for each reachable tag, create a link to the asset
            for reached in reachable:
                link_asset(asset, reached, 1)
                #add the linked tag to the list of tags that have been linked
                linked.append(reached)
    return

#remove implied links from the given asset due to the given tag
def detach_tag(asset):
    #find all edges to the asset that are implied
    impl_edges = AssetEdge.objects.filter(asset_id__exact = asset.id).filter(implied__exact = 1)
    #delete all implied edges
    for edge in impl_edges:
        edge.delete()
    #find all tags directly linked to the asset
    direct_tags = find_asset_tags_direct(asset)
    #create list to store linked tags
    linked = []
    #add direct tags to the list of linked tags
    linked = linked+direct_tags
    #for each direct tag, find all the tags it implies and link them to the asset
    for tag in direct_tags:
        #find all the tags that this tag implies, ignoring tags that have already been linked
        reachable = reachable_child(tag, linked)
        #for each reachable tag, create a link to the asset
        for reached in reachable:
            link_asset(asset, reached, 1)
            #add the linked tag to the list of tags that have been linked
            linked.append(reached)
    return
    
#removes an edge between a given parent and child tag
def remove_edge(parent, child):
    #find the edge with the given parent and child tag
    to_remove = Edge.objects.filter(parent_tag__exact = parent.id).filter(child_tag__exact = child.tag)[0]
    #check that the edge exists
    if to_remove != None:
        #remove the edge
        to_remove.delete()
        #remove any asset links implied because of this edge
        clear_false_links(parent)
    return

#removes an edge between a given asset and tag
def remove_asset_edge(asset, tag):
    #find the edge with the given asset and tag
    to_remove = AssetEdge.objects.filter(asset_id__exact = asset.id).filter(tag_id__exact = tag.id)[0]
    #check that the edge exists
    if to_remove != None:
        #remove the edge
        to_remove.delete()
        #remove any asset links implied because of this edge
        detach_tag(asset)
    return
        




