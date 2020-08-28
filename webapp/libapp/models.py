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
    #Check given tags are in database (only use if input is text(name) based)
    #parTag = tag_by_name(parent)
    #chilTag = tag_by_name(child)
    parTag = parent
    chilTag = child
    newEdge = Edge(parent_tag = parTag.id, child_tag = chilTag.id)
    newEdge.save()
    return

#Given an asset and a tag, link the tag to the asset
def link_asset(asset, tag):
    #Check given tags are in database (only use if input is text(name) based)
    #thisAsset = Asset.objects.filter(name__exact= asset)
    #thisTag = tag_by_name(tag)
    thisAsset = asset
    thisTag = tag
    newEdge = AssetEdge(asset_id = thisAsset.id, tag_id = thisTag.id)
    newEdge.save()
    return

#returns a list of assets with direct links to this tag
def find_assets_direct(tag):
    assets= []
    asset_query = AssetEdge.objects.filter(tag_id__exact=tag.id)
    for link in asset_query:
        this_asset = Asset.objects.filter(id__exact = link.asset_id)[0]
        assets.append(this_asset)
    return assets

#returns a list of tags that imply the given tag
def find_parent_tags(tag, ignore):
    tags = []
    tag_query = Edge.objects.filter(child_tag__exact = tag.id)
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.parent_tag)[0]
        if this_tag.id not in ignore:
            tags.append(this_tag)
    return tags

#returns a list of assets linked to the given tag either directly or implicitly
def find_all_assets(tag):
    #initialise the empty list of assets
    assets = []
    #list to store any tags that have been checked to avoid cycles
    tags_checked = []
    #the list of parent tags that have been found used as a stack
    tags_to_check = []
    #add the given tag to the list of tags to check
    tags_to_check.append(tag)
    #cycle over the list of tags to check until there are no more to check
    while len(tags_to_check) > 0:
        #remove the newest tag from the stack
        checking = tags_to_check.pop(len(tags_to_check)-1)
        #find all parent tags for the current tag
        parents = find_parent_tags(checking, tags_checked)
        #add the current tag to the list of checked tags
        tags_checked.append(checking)
        #add all new parents to the stack to be checked
        tags_to_check = tags_to_check+parents

        #find all assets directly linked to the current tag
        these_assets = find_assets_direct(checking)
        #add found assets to the list of assets
        assets = assets + these_assets