from models.Artist import Artist
from models.Album import Album
from models.User import User
from models.Track import Track
from models.Playlist import Playlist

from models.Album_Artist_Association import album_artist_association_table as aaat
from models.Album_Track_Association import album_track_association_table as atat
from models.Track_Playlist_Association import track_playlist_association_table as tpat
from models.User_Playlist_Association import user_playlist_association_table as upat

from schemas.ArtistSchema import artist_schema, artists_schema
from schemas.AlbumSchema import album_schema, albums_schema
from schemas.UserSchema import user_schema, users_schema
from schemas.TrackSchema import track_schema, tracks_schema
from schemas.PlaylistSchema import playlist_schema, playlists_schema

from main import db
from flask import Blueprint, request, jsonify, abort, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

playlists = Blueprint('playlists', __name__, url_prefix="/playlists")

@playlists.route("/", methods=["GET"])
def playlist_index():
    #Retrieve all playlists
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@playlists.route("/", methods=["POST"])
@jwt_required
def playlist_create():
    #Create a new playlist
    playlist_fields = playlist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_playlist = Playlist()
    new_playlist.playlist_title = playlist_fields["playlist_title"]
    
    user.playlists.append(new_playlist)

    db.session.add(new_playlist)
    db.session.commit()
    
    return jsonify(playlist_schema.dump(new_playlist))

@playlists.route("/<int:id>", methods=["GET"])
@jwt_required
def playlist_show(id):
    #Return a single playlist
    playlist = Playlist.query.get(id)
    return jsonify(playlist_schema.dump(playlist))

@playlists.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def playlist_update(id):
    #Update a playlist
    playlist_fields = playlist_schema.load(request.json)
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        return abort(401, description="Invalid user")

    playlists = Playlist.query.filter_by(id=id)
    
    if playlists.count() != 1:
        return abort(401, description="Unauthorized to update this book")

    playlists.update(playlist_fields)
    db.session.commit()

    return jsonify(playlist_schema.dump(playlists[0]))

@playlists.route("/<int:id>", methods=["DELETE"])
def playlist_delete(id):
    #Delete a playlist
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    playlist = Playlist.query.filter_by(id=id, user_id=user.id).first()

    if not playlist:
        return abort(400)

    db.session.delete(playlist)
    db.session.commit()

    return jsonify(playlist_schema.dump(playlist))