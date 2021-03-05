from models.Artist import Artist
from models.User import User
from models.Album import Album


from main import db
from schemas.ArtistSchema import artist_schema, artists_schema
from schemas.AlbumSchema import album_schema, albums_schema
from flask import Blueprint, request, jsonify, abort, render_template
from models.Album_Artist_Association import album_artist_association_table as aaat
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

artists = Blueprint('artists', __name__, url_prefix="/artists")

@artists.route("/", methods=["GET"])
def artist_index():
    #Retrieve all artists
    artists = Artist.query.options(joinedload("user")).all()
    return render_template("artists.html", artists=artists)

@artists.route("/", methods=["POST"])
@jwt_required
def artist_create():
    #Create a new artist
    artist_fields = artist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")
    
    new_artist = Artist()
    new_artist.artist_name = artist_fields["artist_name"]

    user.artists.append(new_artist)
    
    db.session.add(new_artist)
    db.session.commit()
    
    return jsonify(artist_schema.dump(new_artist))

@artists.route("/<int:id>", methods=["GET"])
@jwt_required
def artist_show(id):
    #Return a single artist
    artist = Artist.query.get(id)
    return jsonify(artist_schema.dump(artist))

##### Ask Alex H to help me fix further later
@artists.route("/albums/<int:id>", methods=["GET"])
@jwt_required
def artist_list_albums(id):
    #Return a single artist's album IDs
    albums = db.session.query(aaat).filter(aaat.c.artist_id == id)
    artist = Artist.query.get(id)
    artist_list_new = []
    art_scheme = artist_schema.dump(artist)
    for album in albums:
        album_scheme = album_schema.dump(Album.query.get(album.album_id))
        artist_list_new.append((art_scheme, album_scheme))
    return jsonify(artist_list_new) 


@artists.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def artist_update(id):
    #Update a artist
    artist_fields = artist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    artists = Artist.query.filter_by(id=id, user_id=user.id)
    
    if artists.count() != 1:
        return abort(401, description="Unauthorized to update this artist")

    artists.update(artist_fields)
    db.session.commit()

    return jsonify(artist_schema.dump(artists[0]))

@artists.route("/<int:id>", methods=["DELETE"])
@jwt_required
def artist_delete(id):
    #Delete a artist
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    artist = Artist.query.filter_by(id=id, user_id=user.id).first()

    if not artist:
        return abort(400)

    db.session.delete(artist)
    db.session.commit()

    return jsonify(artist_schema.dump(artist))