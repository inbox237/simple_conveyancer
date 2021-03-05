
from models.Album_Artist_Association import album_artist_association_table as aaat
from models.Album_Track_Association import album_track_association_table as atat
from models.Track_Playlist_Association import track_playlist_association_table as tpat
from models.User_Playlist_Association import user_playlist_association_table as upat

from models.Album import Album

from schemas.TrackSchema import track_schema, tracks_schema
from schemas.AlbumSchema import album_schema, albums_schema
from schemas.PlaylistSchema import playlist_schema, playlists_schema
from schemas.SeasonalDSchema import seasonald_schema, seasonalds_schema
from schemas.SeasonalPSchema import seasonalp_schema, seasonalps_schema

from main import db
from flask import Blueprint, request, jsonify, abort, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

albums = Blueprint('albums', __name__, url_prefix="/albums")

@albums.route("/", methods=["GET"])
def album_index():
    #Retrieve all albums
    albums = Album.query.all()
    return render_template("albums.html", albums=albums)


@albums.route("/", methods=["POST"])
@jwt_required
def album_create():
    #Create a new album
    album_fields = album_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_album = Album()
    new_album.album_title = album_fields["album_title"]
    
    user.albums.append(new_album)

    db.session.add(new_album)
    db.session.commit()
    
    return jsonify(album_schema.dump(new_album))

@albums.route("/<int:id>", methods=["GET"])
@jwt_required
def album_show(id):
    #Return a single album
    album = Album.query.get(id)
    return jsonify(album_schema.dump(album))

@albums.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def album_update(id):
    #Update a album
    album_fields = album_schema.load(request.json)
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        return abort(401, description="Invalid user")

    albums = Album.query.filter_by(id=id)
    
    if albums.count() != 1:
        return abort(401, description="Unauthorized to update this album")

    albums.update(album_fields)
    db.session.commit()

    return jsonify(album_schema.dump(albums[0]))

@albums.route("/<int:id>", methods=["DELETE"])
def album_delete(id):
    #Delete a album
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    album = Album.query.filter_by(id=id, user_id=user.id).first()

    if not album:
        return abort(400)

    db.session.delete(album)
    db.session.commit()

    return jsonify(album_schema.dump(album))
