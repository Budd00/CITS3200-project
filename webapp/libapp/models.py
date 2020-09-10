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
    newEdge = Edge(parent_tag = parent, child_tag = child)
    newEdge.save()
    return

#Given an asset and a tag, link the tag to the asset
def link_asset(asset, tag):
    #Check given tags are in database (only use if input is text(name) based)
    #thisAsset = Asset.objects.filter(name__exact= asset)
    #thisTag = tag_by_name(tag)
    thisAsset = asset
    thisTag = tag
    newEdge = AssetEdge(asset_id = thisAsset, tag_id = thisTag)
    newEdge.save()
    return

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
        #if the found asset is nt in the "found" list, add it to the assets list
        if this_asset not in found:
            assets.append(this_asset)
    #return the assets list
    return assets

#returns a list of tags with direct links to this asset, ignoring any tags in the ignore list
def find_tags_direct(asset, ignore=[]):
    #empty list to store found tags
    tags= []
    #find all edges linking a tag to the given asset
    tag_query = AssetEdge.objects.filter(asset_id__exact=asset.id)
    #for each edge found, retrieve the tag
    for link in tag_query:
        this_tag = Tag.objects.filter(id__exact = link.tag_id.id)[0]
        #if the found tag is not in the ignore list, add it to the tags list
        if this_tag not in ignore:
            tags.append(this_tag)
    #return the tags list
    return tags

#returns a list of tags that imply the given tag, ignoring any tags in the ignore list
def find_parent_tags(tag, ignore=[]):
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
        these_assets = find_assets_direct(checking, assets)
        #add found assets to the list of assets
        assets = assets + these_assets
    #return the list of found assets
    return assets

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