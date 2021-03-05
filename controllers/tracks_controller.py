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

tracks = Blueprint('tracks', __name__, url_prefix="/tracks")

@tracks.route("/", methods=["GET"])
def track_index():
    #Retrieve all tracks
    tracks = Track.query.all()
    return render_template("tracks.html", tracks=tracks)


@tracks.route("/", methods=["POST"])
@jwt_required
def track_create():
    #Create a new track
    track_fields = track_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_track = Track()
    new_track.track_title = track_fields["track_title"]
    
    user.tracks.append(new_track)

    db.session.add(new_track)
    db.session.commit()
    
    return jsonify(track_schema.dump(new_track))

@tracks.route("/<int:id>", methods=["GET"])
@jwt_required
def track_show(id):
    #Return a single track
    track = Track.query.get(id)
    return jsonify(track_schema.dump(track))

@tracks.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def track_update(id):
    #Update a track
    track_fields = track_schema.load(request.json)
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        return abort(401, description="Invalid user")

    tracks = Track.query.filter_by(id=id)
    
    if tracks.count() != 1:
        return abort(401, description="Unauthorized to update this book")

    tracks.update(track_fields)
    db.session.commit()

    return jsonify(track_schema.dump(tracks[0]))

@tracks.route("/<int:id>", methods=["DELETE"])
def track_delete(id):
    #Delete a track
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    track = Track.query.filter_by(id=id, user_id=user.id).first()

    if not track:
        return abort(400)

    db.session.delete(track)
    db.session.commit()

    return jsonify(track_schema.dump(track))