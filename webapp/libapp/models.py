from django.db import models
import uuid

# Create your models here.
#create asset table
#!!!---Placeholder---!!!
class Asset(models.Model):
    
    #primary key
    id = models.UUIDField(primary_key = True)
    #name
    name = models.CharField(max_length = 64)
    #Any notes for the public to read. ie. description
    pub_notes = models.TextField()
    #Any notes not for the public to read. ie. missing peices, maintenance issues
    priv_notes = mdels.TextField()

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
    parent_tag  = models.ForeignKey(Tag)
    #tag id of the child tag
    child_tag   = models.ForeignKey(Tag)

    #return this edge id
    def __repr__(self):
        return self.id

#Create Asset to tag edges table to track asset tags
class AssetEdge(models.Model):

    #initialise attributes
    #primary key
    id          = models.UUIDField(default=uuid.uuid4, primary_key = True)
    #id of the asset
    asset_id    = models.ForeignKey(Asset)
    #id of linked tag
    tag_id      = models.ForeignKey(Tag)
    
    #return this edge id
    def __repr__(self):
        return self.id


#return a tag object with the given name
def tag_by_name(name):
    #query the database for a tag with the given name
    result = Tag.objects.filter(name__exact= name)
    return result

#return a tag object with the given id
def tag_by_id(id):
    #query the database for a tag with the given id
    result = Tag.objects.filter(id__exact= id)
    return result

#Given two tags, create an edge link from parent to child
def link_tags(parent, child):
    parTag = parent
    chilTag = child
    newEdge = Edge(parent_tag = parTag.id, child_tag = chilTag.id)
    newEdge.save()
    link_assets_new(newEdge)
    return

#Given an asset and a tag, link the tag to the asset
def link_asset(asset, tag):
    #Check given tags are in database (only use if input is text(name) based)
    #thisAsset = Asset.objects.filter(name__exact= asset)
    #thisTag = tag_by_name(tag)
    thisAsset = asset
    thisTag = tag
    #check that there isn't already a link
    #find all edges to the asset
    existingEdges = AssetEdge.objects.filter(asset_id__exact = asset.id)
    #set exists variable to false
    exists = False
    #check each edge to see if the given tag is already linked
    for edge in existingEdges:
        if edge.tag_id == tag.id:
            exists = True
    if !exists:
        newEdge = AssetEdge(asset_id = thisAsset.id, tag_id = thisTag.id)
        newEdge.save()
    return

#returns a list of assets with direct links to this tag, ignoring any assets in the found list
def find_assets_direct(tag, found):
    #empty list to store found assets
    assets= []
    #find all edges linking an asset to the given tag
    asset_query = AssetEdge.objects.filter(tag_id__exact=tag.id)
    #for each edge found, retrieve the asset
    for link in asset_query:
        this_asset = Asset.objects.filter(id__exact = link.asset_id)[0]
        #if the found asset is nt in the "found" list, add it to the assets list
        if this_asset not in found:
            assets.append(this_asset)
    #return the assets list
    return assets

#returns a list of tags with direct links to this asset, ignoring any tags in the ignore list
def find_asset_tags_direct(asset, ignore):
    #empty list to store found tags
    tags= []
    #find all edges linking a tag to the given asset
    tag_query = AssetEdge.objects.filter(asset_id__exact=asset.id)
    #for each edge found, retrieve the tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.tag_id)[0]
        #if the found tag is not in the ignore list, add it to the tags list
        if this_tag not in ignore:
            assets.append(this_tag)
    #return the tags list
    return assets

#returns a list of tags that imply the given tag, ignoring any tags in the ignore list
def find_parent_tags(tag, ignore):
    #empty tags list to store found parent tags
    tags = []
    #find all edges with the given tag as the child tag
    tag_query = Edge.objects.filter(child_tag__exact = tag.id)
    #for each edge found, retreive the parent tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.parent_tag)[0]
        #if the parent tag is not in the ignore list, add it to the tags list
        if this_tag.id not in ignore:
            tags.append(this_tag)
    #return the tags list
    return tags

    #returns a list of tags that the given tag implies, ignoring any tags in the ignore list
def find_child_tags(tag, ignore):
    #empty tags list to store found child tags
    tags = []
    #find all edges with the given tag as the parent tag
    tag_query = Edge.objects.filter(parent_tag__exact = tag.id)
    #for each edge found, retreive the child tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.child_tag)[0]
        #if the child tag is not in the ignore list, add it to the tags list
        if this_tag.id not in ignore:
            tags.append(this_tag)
    #return the tags list
    return tags

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

#finds all assets linked to a parent tag in an edge and links them to all the child tags of that edge
def link_assets_new(edge):
    #create an empty ignore list
    ignore=[]
    #find the parent tag linked to the edge
    this_parent = Tag.objects.filter(id__exact = edge.parent_tag)[0]
    #find the child tag linked to the edge
    this_child =  Tag.objects.filter(id__exact = edge.child_tag)[0]
    #find all assets already linked to the parent tag
    assets = find_assets_direct(this_parent, ignore)
    #find all tags that are children of the child tag
    children = find_child_tags(this_parent, ignore)
    #create a link between each asset and each tag found if non already exists
    for asset in assets:
        for tag in children:
            link_asset(asset, tag)
    return


#check if a tag exists, if it doesn't, create one. returns the found/created tag
def add_tag(name):
    #search for a tag with the given name
    newtag = Tag.objects.filter(name__exact = name)[0]
    #if the tag doesn't exist, create a new one
    if newtag == None:
        newtag = Tag(name=name)
        newtag.save()
    #return the tag with the given name
    return newtag
    