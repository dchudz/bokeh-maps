import numpy as np

def get_zoom_level(bounds, map_dim):
# based on
#  http://stackoverflow.com/questions/6048975/google-maps-v3-how-to-calculate-the-zoom-level-for-a-given-bounds
# function getBoundsZoomLevel(bounds, mapDim) {
#     var WORLD_DIM = { height: 256, width: 256 };
#     var ZOOM_MAX = 21;

#     function latRad(lat) {
#         var sin = Math.sin(lat * Math.PI / 180);
#         var radX2 = Math.log((1 + sin) / (1 - sin)) / 2;
#         return Math.max(Math.min(radX2, Math.PI), -Math.PI) / 2;
#     }

#     function zoom(mapPx, worldPx, fraction) {
#         return Math.floor(Math.log(mapPx / worldPx / fraction) / np.log(2));
#     }

#     var ne = bounds.getNorthEast();
#     var sw = bounds.getSouthWest();

#     var latFraction = (latRad(ne.lat()) - latRad(sw.lat())) / Math.PI;

#     var lngDiff = ne.lng() - sw.lng();
#     var lngFraction = ((lngDiff < 0) ? (lngDiff + 360) : lngDiff) / 360;

#     var latZoom = zoom(mapDim.height, WORLD_DIM.height, latFraction);
#     var lngZoom = zoom(mapDim.width, WORLD_DIM.width, lngFraction);

#     return Math.min(latZoom, lngZoom, ZOOM_MAX);
# }

    world_dim = {"height": 256, "width": 256}
    max_zoom_level = 21

    def lat_rad(lat):
        sin = np.sin(lat * np.pi)
        rad_x2 = np.log((1+sin) / (1-sin)) / 2
        return np.max(np.min(rad_x2, np.pi), -1 * np.pi) / 2

    def zoom(mapPx, worldPx, fraction):
        return np.floor(np.log(map_px/world_px/fraction) / np.log(2))

    #Need to finish work below    
