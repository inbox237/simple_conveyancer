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

seasonalps = Blueprint('seasonalps', __name__, url_prefix="/seasonalps")

@seasonalps.route("/", methods=["GET"])
def seasonalp_index():
    #Retrieve all seasonalps
    seasonalps = SeasonalP.query.all()
    return render_template("seasonalps.html", seasonalps=seasonalps)


@seasonalps.route("/", methods=["POST"])
@jwt_required
def seasonalp_create():
    #Create a new seasonalp
    seasonalp_fields = seasonalp_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_seasonalp = SeasonalP()
    new_seasonalp.seasonalp_title = seasonalp_fields["seasonalp_title"]
    
    user.seasonalps.append(new_seasonalp)

    db.session.add(new_seasonalp)
    db.session.commit()
    
    return jsonify(seasonalp_schema.dump(new_seasonalp))

@seasonalps.route("/<int:id>", methods=["GET"])
@jwt_required
def seasonalp_show(id):
    #Return a single seasonalp
    seasonalp = SeasonalP.query.get(id)
    return jsonify(seasonalp_schema.dump(seasonalp))

@seasonalps.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def seasonalp_update(id):
    #Update a seasonalp
    seasonalp_fields = seasonalp_schema.load(request.json)
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)    

    if not user:
        return abort(401, description="Invalid user")

    seasonalps = SeasonalP.query.filter_by(id=id)
    
    if seasonalps.count() != 1:
        return abort(401, description="Unauthorized to update this book")

    seasonalps.update(seasonalp_fields)
    db.session.commit()

    return jsonify(seasonalp_schema.dump(seasonalps[0]))

@seasonalps.route("/<int:id>", methods=["DELETE"])
def seasonalp_delete(id):
    #Delete a seasonalp
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    seasonalp = SeasonalP.query.filter_by(id=id, user_id=user.id).first()

    if not seasonalp:
        return abort(400)

    db.session.delete(seasonalp)
    db.session.commit()

    return jsonify(seasonalp_schema.dump(seasonalp))