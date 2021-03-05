from models.Artist import Artist
from models.Album import Album
from models.User import User
from models.Track import Track
from models.Playlist import Playlist
from models.SeasonalD import SeasonalD

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

seasonalds = Blueprint('seasonalds', __name__, url_prefix="/seasonalds")

@seasonalds.route("/", methods=["GET"])
def seasonald_index():
    #Retrieve all seasonalds
    seasonalds = SeasonalD.query.all()
    return render_template("seasonalds.html", seasonalds=seasonalds)


@seasonalds.route("/", methods=["POST"])
@jwt_required
def seasonald_create():
    #Create a new seasonald
    seasonald_fields = seasonald_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_seasonald = SeasonalD()
    new_seasonald.seasonald_title = seasonald_fields["seasonald_title"]
    
    user.seasonalds.append(new_seasonald)

    db.session.add(new_seasonald)
    db.session.commit()
    
    return jsonify(seasonald_schema.dump(new_seasonald))

@seasonalds.route("/<int:id>", methods=["GET"])
@jwt_required
def seasonald_show(id):
    #Return a single seasonald
    seasonald = SeasonalD.query.get(id)
    return jsonify(seasonald_schema.dump(seasonald))

@seasonalds.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def seasonald_update(id):
    #Update a seasonald
    seasonald_fields = seasonald_schema.load(request.json)
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        return abort(401, description="Invalid user")

    seasonalds = SeasonalD.query.filter_by(id=id)
    
    if seasonalds.count() != 1:
        return abort(401, description="Unauthorized to update this book")

    seasonalds.update(seasonald_fields)
    db.session.commit()

    return jsonify(seasonald_schema.dump(seasonalds[0]))

@seasonalds.route("/<int:id>", methods=["DELETE"])
def seasonald_delete(id):
    #Delete a seasonald
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    seasonald = SeasonalD.query.filter_by(id=id, user_id=user.id).first()

    if not seasonald:
        return abort(400)

    db.session.delete(seasonald)
    db.session.commit()

    return jsonify(seasonald_schema.dump(seasonald))