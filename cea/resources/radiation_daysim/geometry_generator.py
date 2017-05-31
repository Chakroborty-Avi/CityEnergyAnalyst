"""
Geometry generator from
Shapefiles (buiding footprint)
and .tiff (terrain)

into 3D geometry with windows and roof equivalent to LOD3

"""
import pyliburo.py3dmodel.construct as construct
import pyliburo.py3dmodel.fetch as fetch
import pyliburo.py3dmodel.calculate as calculate
import pyliburo.py3dmodel.modify as modify
import pyliburo.pycitygml as pycitygml
import pyliburo.gml3dmodel as gml3dmodel
import pyliburo.shp2citygml as shp2citygml

from OCC.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCC.gp import gp_Pnt, gp_Lin, gp_Ax1, gp_Dir
from geopandas import GeoDataFrame as gdf
import shapefile
import cea.globalvar
import cea.inputlocator
import numpy as np
import gdal
import time

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Kian Wee Chen"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def identify_surfaces_type(occface_list):

    facade_list = []
    roof_list = []
    footprint_list = []
    vec1 = (0, 0, 1)

    # distinguishing between facade, roof and footprint.
    for f in occface_list:
        # get the normal of each face
        n = py3dmodel.calculate.face_normal(f)
        angle = py3dmodel.calculate.angle_bw_2_vecs(vec1, n)
        # means its a facade
        if angle > 45 and angle < 135:
            facade_list.append(f)
        elif angle <= 45:
            roof_list.append(f)
        elif angle >= 135:
            footprint_list.append(f)

    facade_list_north = []
    roof_list = []
    footprint_list = []
    vec1 = (0, 0, 1)
    for f in facade_list:


    return facade_list_north, facade_list_west, facade_list_east, facade_list_south, roof_list, footprint_list


def calc_intersection(terrain_intersection_curves, edges_coords, edges_dir):
    """
    This script calculates the intersection of the building edges to the terrain,
    :param terrain_intersection_curves:
    :param edges_coords:
    :param edges_dir:
    :return:
            intersecting points, intersecting faces
    """
    building_line = gp_Lin(gp_Ax1(gp_Pnt(edges_coords[0], edges_coords[1], edges_coords[2]),
                                  gp_Dir(edges_dir[0], edges_dir[1], edges_dir[2])))
    terrain_intersection_curves.PerformNearest(building_line, 0.0, float("+inf"))
    if terrain_intersection_curves.IsDone():
        npts = terrain_intersection_curves.NbPnt()
        if npts !=0:
            return terrain_intersection_curves.Pnt(1), terrain_intersection_curves.Face(1)
        else:
            return None, None
    else:
        return None, None

def create_windows(surface, wwr, ref_pypt):
    return fetch.shape2shapetype(modify.uniform_scale(surface, wwr, wwr, wwr, ref_pypt))

def create_hollowed_facade(surface_facade, window):
    b_facade_cmpd = fetch.shape2shapetype(construct.boolean_difference(surface_facade, window))
    hole_facade = fetch.geom_explorer(b_facade_cmpd, "face")[0]
    hollowed_facade = construct.simple_mesh(hole_facade)

    return hollowed_facade, hole_facade

def building2d23d(zone_shp_path, district_shp_path, tin_occface_list, architecture_path,
                  height_col, nfloor_col):
    """
    This script extrudes buildings from the shapefile and creates intermediate floors.

    :param district_shp_path: path to the shapefile to be extruded of the district
    :param tin_occface_list: the faces of the terrain, to be used to put the buildings on top.
    :param height_col:
    :param nfloor_col:
    :return:
    """
    # read district shapefile and names of buildings of the zone of analysis
    district_building_records = gdf.from_file(district_shp_path).set_index('Name')
    district_building_names = district_building_records.index.values
    zone_building_names = gdf.from_file(zone_shp_path)['Name'].values
    architecture_wwr = gdf.from_file(architecture_path)

    #make shell out of tin_occface_list and create OCC object
    terrain_shell = construct.make_shell_frm_faces(tin_occface_list)[0]
    terrain_intersection_curves = IntCurvesFace_ShapeIntersector()
    terrain_intersection_curves.Load(terrain_shell, 1e-6)

    #empty list where to store the closed geometries
    bsolid_list = []

    for name in district_building_names:
        height = float(district_building_records.loc[name, height_col])
        nfloors = int(district_building_records.loc[name, nfloor_col])

        # simplify geometry tol =1 for buildings of interest, tol = 5 for surroundings
        if name in zone_building_names:
            range_floors = range(nfloors+1)
            flr2flr_height = height / nfloors
            geometry = district_building_records.ix[name].geometry.simplify(1, preserve_topology=True)
        else:
            range_floors = [0,1]
            flr2flr_height = height
            geometry = district_building_records.ix[name].geometry.simplify(5, preserve_topology=True)


        point_list_2D = list(geometry.exterior.coords)
        point_list_3D = [(a,b,0) for (a,b) in point_list_2D] # add 0 elevation

        #creating floor surface in pythonocc
        face = construct.make_polygon(point_list_3D)
        #get the midpt of the face
        face_midpt = calculate.face_midpt(face)

        #project the face_midpt to the terrain and get the elevation
        inter_pt, inter_face = calc_intersection(terrain_intersection_curves, face_midpt, (0, 0, 1))

        loc_pt = fetch.occpt2pypt(inter_pt)
        #reconstruct the footprint with the elevation
        face = fetch.shape2shapetype(modify.move(face_midpt, loc_pt, face))

        moved_face_list = []
        for floor_counter in range_floors:
            dist2mve = floor_counter*flr2flr_height
            #get midpt of face
            orig_pt = calculate.face_midpt(face)
            #move the pt 1 level up
            dest_pt = modify.move_pt(orig_pt, (0,0,1), dist2mve)
            moved_face = modify.move(orig_pt, dest_pt, face)
            moved_face_list.append(moved_face)

        #loft all the faces and form a solid
        vertical_shell = construct.make_loft(moved_face_list)
        vertical_face_list = fetch.geom_explorer(vertical_shell, "face")
        roof = moved_face_list[-1]
        footprint = moved_face_list[0]
        all_faces = []
        all_faces.append(footprint)
        all_faces.extend(vertical_face_list)
        all_faces.append(roof)
        bldg_shell_list = construct.make_shell_frm_faces(all_faces)

        if bldg_shell_list:
            # make sure all the normals are correct (they are pointing out)
            bldg_solid = construct.make_solid(bldg_shell_list[0])
            bldg_solid = modify.fix_close_solid(bldg_solid)

            # identify building surfaces according to angle:
            face_list = py3dmodel.fetch.faces_frm_solid(bldg_solid)
            facade_list, roof_list, footprint_list = identify_surfaces_type(face_list)


            facade_list, roof_list, footprint_list = gml3dmodel.identify_building_surfaces(bldg_solid)

            # calculate windows in facade_list
            if name in zone_building_names:
                # get window properties
                wwr_west = architecture_wwr.loc[name,"wwr_west"]
                wwr_east = architecture_wwr.loc[name,"wwr_east"]
                wwr_north = architecture_wwr.loc[name,"wwr_north"]
                wwr_south = architecture_wwr.loc[name,"wwr_south"]

                for surface_facade in facade_list:

                    ref_pypt = calculate.face_midpt(surface_facade)
                    # offset the facade to create a window according to the wwr
                    if 0.0 < wwr < 1.0:
                        window = create_windows(surface_facade, wwr, ref_pypt)
                        create_radiance_srf(window, "win" + str(bcnt) + str(fcnt),
                                            "win" + str(ageometry_table['type_win'][bldg_name]), rad)
                        window_list.append(window)

                        # triangulate the wall with hole
                        hollowed_facade, hole_facade = create_hollowed_facade(surface_facade,
                                                                              window)  # accounts for hole created by window
                        wall_list.append(hole_facade)

                        # check the elements of the wall do not have 0 area and send to radiance
                        for triangle in hollowed_facade:
                            tri_area = calculate.face_area(triangle)
                            if tri_area > 1E-3:
                                create_radiance_srf(triangle, "wall" + str(bcnt) + str(fcnt),
                                                    "wall" + str(ageometry_table['type_wall'][bldg_name]), rad)








            bsolid_list.append(bldg_solid)

        #identify building surfaces according to angle:


    return bsolid_list

def buildings2radiance(rad, ageometry_table):

        facade_list, roof_list, footprint_list = gml3dmodel.identify_building_surfaces(bldg_solid)
        wall_list = []
        wwr = ageometry_table["win_wall"][bldg_name]

        for fcnt, surface_facade in enumerate(facade_list):
            ref_pypt = calculate.face_midpt(surface_facade)

            # offset the facade to create a window according to the wwr
            if 0.0 < wwr < 1.0:
                window = create_windows(surface_facade, wwr, ref_pypt)
                create_radiance_srf(window, "win" + str(bcnt) + str(fcnt),
                                    "win" + str(ageometry_table['type_win'][bldg_name]), rad)
                window_list.append(window)

                # triangulate the wall with hole
                hollowed_facade, hole_facade = create_hollowed_facade(surface_facade,
                                                                      window)  # accounts for hole created by window
                wall_list.append(hole_facade)

                # check the elements of the wall do not have 0 area and send to radiance
                for triangle in hollowed_facade:
                    tri_area = calculate.face_area(triangle)
                    if tri_area > 1E-3:
                        create_radiance_srf(triangle, "wall" + str(bcnt) + str(fcnt),
                                            "wall" + str(ageometry_table['type_wall'][bldg_name]), rad)

            elif wwr == 1.0:
                create_radiance_srf(surface_facade, "win" + str(bcnt) + str(fcnt),
                                    "win" + str(ageometry_table['type_win'][bldg_name]), rad)
                window_list.append(surface_facade)
            else:
                create_radiance_srf(surface_facade, "wall" + str(bcnt) + str(fcnt),
                                    "wall" + str(ageometry_table['type_wall'][bldg_name]), rad)
                wall_list.append(surface_facade)

        for rcnt, roof in enumerate(roof_list):
            create_radiance_srf(roof, "roof" + str(bcnt) + str(rcnt),
                                "roof" + str(ageometry_table['type_roof'][bldg_name]), rad)

        bldg_dict["name"] = bldg_name
        bldg_dict["windows"] = window_list
        bldg_dict["walls"] = wall_list
        bldg_dict["roofs"] = roof_list
        bldg_dict["footprints"] = footprint_list
        bldg_dict_list.append(bldg_dict)

    return bldg_dict_list

def raster2tin(input_terrain_raster):

    # read raster records
    raster_dataset = gdal.Open(input_terrain_raster)
    band = raster_dataset.GetRasterBand(1)
    a = band.ReadAsArray(0, 0, raster_dataset.RasterXSize, raster_dataset.RasterYSize)
    (y_index, x_index) = np.nonzero(a >= 0)
    (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = raster_dataset.GetGeoTransform()
    x_coords = x_index * x_size + upper_left_x + (x_size / 2)  # add half the cell size
    y_coords = y_index * y_size + upper_left_y + (y_size / 2)  # to centre the point

    raster_points = [(x, y, z) for x, y, z in zip(x_coords, y_coords, a[y_index, x_index])]

    tin_occface_list = construct.delaunay3d(raster_points)

    return tin_occface_list


def geometry_main(zone_shp_path, district_shp_path, input_terrain_raster, architecture_path):

    # transform terrain from raster to tin
    geometry_terrain = raster2tin(input_terrain_raster)
    
    # transform buildings 2D to 3D and add windows
    geometry_buildings = building2d23d(zone_shp_path, district_shp_path, geometry_terrain, architecture_path,
                                height_col='height_ag', nfloor_col="floors_ag")

    return geometry_terrain, geometry_buildings

if __name__ == '__main__':

    # import modules
    gv = cea.globalvar.GlobalVariables()
    scenario_path = gv.scenario_reference
    locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)

    # local variables
    output_folder = locator.get_building_geometry_citygml()
    district_shp = locator.get_district()
    zone_shp = locator.get_building_geometry()
    architecture_dbf = locator.get_building_architecture()
    input_terrain_raster = locator.get_terrain()

    # run routine City GML LOD 1
    time1 = time.time()
    geometry_terrain, geometry_buildings = geometry_main(zone_shp, district_shp, input_terrain_raster, architecture_dbf)
    print "Geometry of the scene created in", (time.time() - time1) / 60.0, " mins"

    # to visualize the results
    #construct.visualise([geometry_terrain,geometry_buildings], ["GREEN","WHITE"], backend = "wx") #install Wxpython



