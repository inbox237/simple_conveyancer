from controllers.albums_controller import albums
from controllers.artists_controller import artists
from controllers.auth_controller import auth
from controllers.tracks_controller import tracks
from controllers.playlists_controller import playlists
from controllers.seasonalds_controller import seasonalds
from controllers.seasonalps_controller import seasonalps

registerable_controllers = [
    auth,
    albums,
    artists,
    tracks,
    playlists,
    seasonalds,
    seasonalps
]