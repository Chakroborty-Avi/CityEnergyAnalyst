from __future__ import division
import utm
from geopandas import GeoDataFrame as gdf

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

def shapefile_to_WSG_and_UTM(shapefile_path):

    #read the CPG and repalce whateever is there with ISO, and save
    cpg_file_path = shapefile_path.split('.shp', 1)[0] + '.CPG'
    cpg_file = open(cpg_file_path, "w")
    cpg_file.write("ISO-8859-1")
    cpg_file.close()

    # get coordinate system and project to WSG 84
    data = gdf.from_file(shapefile_path)
    data = data.to_crs(epsg=4326)
    lon = data.geometry[0].centroid.coords.xy[0][0]
    lat = data.geometry[0].centroid.coords.xy[1][0]

    # get coordinate system and re project to UTM
    utm_data = utm.from_latlon(lat, lon)
    zone = utm_data[2]
    south_or_north = utm_data[3]
    code_projection = "+proj=utm +zone=" + str(zone)+south_or_north + " +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    data = data.to_crs(code_projection)
    data.to_file(shapefile_path, driver='ESRI Shapefile')

    return data

def raster_to_WSG_and_UTM(raster_path):