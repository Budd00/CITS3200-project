# Currently based on Flask structures, will be edited to suit django if the switch is made



from app import db

#create asset table
#!!!---Placeholder---!!!
class Asset(db.Model):
    #primary key
    id = db.Column(db.Integer, primary_key = True)
    #name
    name = db.Column(db.String(64))

    #Establish relationship to assetedge table
    edges = db.relationship('AssetEdge', backref='asset', lazy='dynamic')

#Create tag table
class Tag(db.Model):

    #Initialise attributes
    #primary key
    id          = db.Column(db.Integer, primary_key = True)
    #tag name
    name        = db.Column(db.String(64), unique=True)
    #Number of times searched
    popularity  = db.Column(db.Integer)

    #Establish relationship to edge tables
    edges = db.relationship('Edge', backref='tag', lazy='dynamic')
    asset_links = db.relationship('AssetEdge', backref='tag', lazy='dynamic')

    #return this tag name
    def __repr__(self):
        return '<Tag {}>'.format(self.name)

    #increase the popularity
    def increase_pop(self):
        self.popularity += 1

#Create tag edges table to track the connections in the graph
class Edge(db.Model):

    #initilise attributes
    #primary key
    id          = db.Column(db.Integer, primary_key = True)
    #tag id of the parent tag
    parent_tag  = db.Column(db.Integer, db.foreignkey('tag.id'))
    #tag id of the child tag
    child_tag   = db.Column(db.Integer, db.foreignkey('tag.id'))

    #return this edge id
    def __repr__(self):
        return '<Edge {}>'.format(self.id)

#Create Asset to tag edges table to track asset tags
class AssetEdge(db.Model):

    #initialise attributes
    #primary key
    id          = db.Column(db.Integer, primary_key = True)
    #id of the asset
    asset_id    = db.Column(db.Integer, db.foreignkey('asset.id'))
    #id of linked tag
    tag_id      = db.Column(db.Integer, db.foreignkey('tag.id'))
    
    #return this edge id
    def __repr__(self):
        return '<AssetEdge {}>'.format(self.id)


#return a tag object with the given name
def tag_by_name(name):
    #query the database for a tag with the given name
    result = Tag.query.filter_by(name = name)
    return result

#return a tag object with the given id
def tag_by_id(id):
    #query the database for a tag with the given id
    result = Tag.query.filter_by(id = id)
    return result

#Given two tags, create an edge link from parent to child
def link_tags(parent, child):
    #Check given tags are in database (only use if input is text(name) based)
    #parTag = tag_by_name(parent)
    #chilTag = tag_by_name(child)
    parTag = parent
    chilTag = child
    newEdge = Edge(parent_tag = parTag.id, child_tag = chilTag.id)
    db.session.add(newEdge)
    db.session.commit()

#Given an asset and a tag, link the tag to the asset
def link_asset(asset, tag):
    #Check given tags are in database (only use if input is text(name) based)
    #thisAsset = Asset.query.filter_by(name = asset)
    #thisTag = tag_by_name(tag)
    thisAsset = asset
    thisTag = tag
    newEdge = AssetEdge(asset_id = thisAsset.id, tag_ig = thisTag.id)
    db.session.add(newEdge)
    db.session.commit()
