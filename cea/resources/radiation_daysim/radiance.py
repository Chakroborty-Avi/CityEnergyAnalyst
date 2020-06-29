import math
import os
import shutil
import subprocess

from collections import deque

from cea import suppres_3rd_party_debug_loggers
suppres_3rd_party_debug_loggers()

import py4design.py2radiance as py2radiance
from py4design.py3dmodel.fetch import points_frm_occface

from cea.resources.radiation_daysim.geometry_generator import BuildingGeometry


class CEARad(py2radiance.Rad):
    """Overrides some methods of py4design.rad that run DAYSIM commands"""
    def __init__(self, base_file_path, data_folder_path, debug=False):
        super(CEARad, self).__init__(base_file_path, data_folder_path)
        self.surfaces = deque()
        self.debug = debug

    def run_cmd(self, cmd, cwd=None):
        # Verbose output if debug is true
        print('Running command `{}`{}'.format(cmd, '' if cwd is None else ' in `{}`'.format(cwd)))
        try:
            # Stops script if commands fail (i.e non-zero exit code)
            subprocess.check_call(cmd, cwd=cwd, stderr=subprocess.STDOUT, env=os.environ)
        except TypeError as error:
            if error.message == "environment can only contain strings":
                for key in os.environ.keys():
                    value = os.environ[key]
                    if not isinstance(value, str):
                        print("Bad ENVIRON key: {key}={value} ({value_type})".format(
                            key=key, value=value, value_type=type(value)))
            raise error

    def execute_epw2wea(self, epwweatherfile, ground_reflectance=0.2):
        daysimdir_wea = self.daysimdir_wea
        if daysimdir_wea == None:
            raise NameError("run .initialise_daysim function before running execute_epw2wea")
        head, tail = os.path.split(epwweatherfile)
        wfilename_no_extension = tail.replace(".epw", "")
        weaweatherfilename = wfilename_no_extension + "_60min.wea"
        weaweatherfile = os.path.join(daysimdir_wea, weaweatherfilename)
        command1 = 'epw2wea "{}" "{}"'.format(epwweatherfile, weaweatherfile)
        f = open(self.command_file, "a")
        f.write(command1)
        f.write("\n")
        f.close()

        # TODO: Might not need `shell`. Check on a Windows machine that has a space in the username
        proc = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
        site_headers = proc.stdout.read()
        site_headers_list = site_headers.split("\r\n")
        hea_filepath = self.hea_file
        hea_file = open(hea_filepath, "a")
        for site_header in site_headers_list:
            if site_header:
                hea_file.write("\n" + site_header)

        hea_file.write("\nground_reflectance" + " " + str(ground_reflectance))
        # get the directory of the long weatherfile
        hea_file.write("\nwea_data_file" + " " + os.path.join(head, wfilename_no_extension + "_60min.wea"))
        hea_file.write("\ntime_step" + " " + "60")
        hea_file.write("\nwea_data_short_file" + " " + os.path.join("wea", wfilename_no_extension + "_60min.wea"))
        hea_file.write("\nwea_data_short_file_units" + " " + "1")
        hea_file.write("\nlower_direct_threshold" + " " + "2")
        hea_file.write("\nlower_diffuse_threshold" + " " + "2")
        hea_file.close()
        # check for the sunuphours
        results = open(weaweatherfile, "r")
        result_lines = results.readlines()
        result_lines = result_lines[6:]
        sunuphrs = 0
        for result in result_lines:
            words = result.replace("\n", "")
            words1 = words.split(" ")
            direct = float(words1[-1])
            diffuse = float(words1[-2])
            total = direct + diffuse
            if total > 0:
                sunuphrs = sunuphrs + 1

        results.close()
        self.sunuphrs = sunuphrs

    def execute_radfiles2daysim(self):
        hea_filepath = self.hea_file
        head, tail = os.path.split(hea_filepath)
        radfilename = tail.replace(".hea", "")
        radgeomfilepath = self.rad_file_path
        radmaterialfile = self.base_file_path
        if radgeomfilepath == None or radmaterialfile == None:
            raise NameError("run .create_rad function before running radfiles2daysim")

        hea_file = open(hea_filepath, "a")
        hea_file.write("\nmaterial_file" + " " + os.path.join("rad", radfilename + "_material.rad"))
        hea_file.write("\ngeometry_file" + " " + os.path.join("rad", radfilename + "_geometry.rad"))
        hea_file.write("\nradiance_source_files 2," + radgeomfilepath + "," + radmaterialfile)
        hea_file.close()
        command1 = 'radfiles2daysim "{}" -g -m -d'.format(hea_filepath)
        f = open(self.command_file, "a")
        f.write(command1)
        f.write("\n")
        f.close()
        self.run_cmd(command1)

    def execute_gen_dc(self, output_unit):
        hea_filepath = self.hea_file
        hea_file = open(hea_filepath, "a")
        sensor_filepath = self.sensor_file_path
        if sensor_filepath == None:
            raise NameError(
                "run .set_sensor_points and create_sensor_input_file function before running execute_gen_dc")

        daysim_pts_dir = self.daysimdir_pts
        if daysim_pts_dir == None:
            raise NameError("run .initialise_daysim function before running execute_gen_dc")

        # first specify the sensor pts
        sensor_filename = os.path.basename(sensor_filepath)
        # move the pts file to the daysim folder
        dest_filepath = os.path.join(daysim_pts_dir, sensor_filename)
        shutil.move(sensor_filepath, dest_filepath)
        # write the sensor file location into the .hea
        hea_file.write("\nsensor_file {rel_sensor_filename}".format(
            rel_sensor_filename=os.path.join("pts", sensor_filename)))
        # write the shading header
        self.write_static_shading(hea_file)
        # write analysis result file
        nsensors = len(self.sensor_positions)
        sensor_str = ""
        if output_unit == "w/m2":
            hea_file.write("\noutput_units" + " " + "1")
            for scnt in range(nsensors):
                # 0 = lux, 2 = w/m2
                if scnt == nsensors - 1:
                    sensor_str = sensor_str + "2"
                else:
                    sensor_str = sensor_str + "2 "

        if output_unit == "lux":
            hea_file.write("\noutput_units" + " " + "2")
            for scnt in range(nsensors):
                # 0 = lux, 2 = w/m2
                if scnt == nsensors - 1:
                    sensor_str = sensor_str + "0"
                else:
                    sensor_str = sensor_str + "0 "

        hea_file.write("\nsensor_file_unit " + sensor_str)

        hea_file.close()
        # copy the .hea file into the tmp directory
        with open(hea_filepath, "r") as hea_file_read:
            lines = hea_file_read.readlines()

        tmp_directory = os.path.join(self.daysimdir_tmp, "")

        # update path to tmp_directory in temp_hea_file
        lines_modified = []
        for line in lines:
            if line.startswith('tmp_directory'):
                lines_modified.append('tmp_directory {}\n'.format(tmp_directory))
            else:
                lines_modified.append(line)

        hea_basename = os.path.splitext(os.path.basename(hea_filepath))[0]
        temp_hea_filepath = os.path.join(self.daysimdir_tmp, hea_basename + "temp.hea")

        with open(temp_hea_filepath, "w") as temp_hea_file:
            temp_hea_file.write('\n'.join(lines_modified))

        # execute gen_dc
        command1 = 'gen_dc "{}" -dir'.format(temp_hea_filepath)
        command2 = 'gen_dc "{}" -dif'.format(temp_hea_filepath)
        command3 = 'gen_dc "{}" -paste'.format(temp_hea_filepath)
        f = open(self.command_file, "a")
        f.write(command1)
        f.write("\n")
        f.write(command2)
        f.write("\n")
        f.write(command3)
        f.write("\n")
        f.close()
        self.run_cmd(command1)
        self.run_cmd(command2)
        self.run_cmd(command3)

    def execute_ds_illum(self):
        hea_filepath = self.hea_file
        head, tail = os.path.split(hea_filepath)

        # execute ds_illum
        command1 = 'ds_illum "{}"'.format(hea_filepath)
        f = open(self.command_file, "a")
        f.write(command1)
        f.write("\n")
        f.close()
        self.run_cmd(command1)


class RadSurface(object):
    """
    An object that contains all the surface information running a Radiance/Daysim simulation.

    :param str name: Name of surface
    :param OCC.TopoDS.TopoDS_Face occ_face: Polygon (OCC TopoDS_Face) of surface
    :param str material: Name of material
    """
    __slots__ = ['name', 'points', 'material']

    def __init__(self, name, occ_face, material):
        self.name = name
        self.points = points_frm_occface(occ_face)
        self.material = material

    def rad(self):
        """
        Returns surface information as Radiance string format.

        Format from Radiance manual:
        `modifier` `type` `identifier`
        `number of string arguments` `string arguments`
        `number of integer arguments` `integer arguments`
        `number of decimal arguments` `decimal arguments`

        In this case,
        `modifier` would be the name of the material
        `type` would be 'polygon'
        there will be no string or integer arguments
        decimal arguments would be points of vertices

        :returns str: The surface written into radiance readable string.
        """

        num_of_points = len(self.points) * 3
        points = ""
        for point in self.points:
            points = points + "{point_x}  {point_y}  {point_z}\n".format(point_x=point[0], point_y=point[1],
                                                                         point_z=point[2])
        surface = "{material} polygon {name}\n" \
                  "0\n" \
                  "0\n" \
                  "{num_of_points}\n" \
                  "{points}".format(material=self.material, name=self.name, num_of_points=num_of_points, points=points)
        return surface


def calc_transmissivity(G_value):
    """
    Calculate window transmissivity from its transmittance using an empirical equation from Radiance.

    :param float G_value: Solar energy transmittance of windows (dimensionless)
    :return float: Transmissivity

    [RADIANCE, 2010] The Radiance 4.0 Synthetic Imaging System. Lawrence Berkeley National Laboratory.
    """
    return (math.sqrt(0.8402528435 + 0.0072522239 * G_value * G_value) - 0.9166530661) / 0.0036261119 / G_value


def add_rad_mat(daysim_mat_file, ageometry_table):
    file_path = daysim_mat_file
    roughness = 0.02
    specularity = 0.03
    with open(file_path, 'w') as write_file:
        # first write the material use for the terrain and surrounding buildings
        string = "void plastic reflectance0.2\n0\n0\n5 0.5360 0.1212 0.0565 0 0"
        write_file.writelines(string + '\n')

        written_mat_name_list = []
        for geo in ageometry_table.index.values:
            mat_name = "wall_" + str(ageometry_table['type_wall'][geo])
            if mat_name not in written_mat_name_list:
                mat_value1 = ageometry_table['r_wall'][geo]
                mat_value2 = mat_value1
                mat_value3 = mat_value1
                mat_value4 = specularity
                mat_value5 = roughness
                string = "void plastic " + mat_name + "\n0\n0\n5 " + str(mat_value1) + " " + str(
                    mat_value2) + " " + str(mat_value3) \
                         + " " + str(mat_value4) + " " + str(mat_value5)

                write_file.writelines('\n' + string + '\n')

                written_mat_name_list.append(mat_name)

            mat_name = "win_" + str(ageometry_table['type_win'][geo])
            if mat_name not in written_mat_name_list:
                mat_value1 = calc_transmissivity(ageometry_table['G_win'][geo])
                mat_value2 = mat_value1
                mat_value3 = mat_value1

                string = "void glass " + mat_name + "\n0\n0\n3 " + str(mat_value1) + " " + str(mat_value2) + " " + str(
                    mat_value3)
                write_file.writelines('\n' + string + '\n')
                written_mat_name_list.append(mat_name)

            mat_name = "roof_" + str(ageometry_table['type_roof'][geo])
            if mat_name not in written_mat_name_list:
                mat_value1 = ageometry_table['r_roof'][geo]
                mat_value2 = mat_value1
                mat_value3 = mat_value1
                mat_value4 = specularity
                mat_value5 = roughness

                string = "void plastic " + mat_name + "\n0\n0\n5 " + str(mat_value1) + " " + str(
                    mat_value2) + " " + str(mat_value3) \
                         + " " + str(mat_value4) + " " + str(mat_value5)
                write_file.writelines('\n' + string + '\n')
                written_mat_name_list.append(mat_name)

        write_file.close()


def terrain_to_radiance(tin_occface_terrain):
    return [RadSurface("terrain_srf" + str(num), face,  "reflectance0.2")
            for num, face in enumerate(tin_occface_terrain)]


def zone_building_to_radiance(building_geometry, building_surface_properties):
    building_name = building_geometry.name
    building_surfaces = []

    # windows
    for num, occ_face in enumerate(building_geometry.windows):
        surface_name = "win_{building_name}_{num}".format(building_name=building_name, num=num)
        material_name = "win_{material}".format(material=building_surface_properties['type_win'][building_name])
        building_surfaces.append(RadSurface(surface_name, occ_face, material_name))

    # walls
    for num, occ_face in enumerate(building_geometry.walls):
        surface_name = "wall_{building_name}_{num}".format(building_name=building_name, num=num)
        material_name = "wall_{material}".format(material=building_surface_properties['type_wall'][building_name])
        building_surfaces.append(RadSurface(surface_name, occ_face, material_name))

    # roofs
    for num, occ_face in enumerate(building_geometry.roofs):
        surface_name = "roof_{building_name}_{num}".format(building_name=building_name, num=num)
        material_name = "roof_{material}".format(material=building_surface_properties['type_roof'][building_name])
        building_surfaces.append(RadSurface(surface_name, occ_face, material_name))

    return building_surfaces


def surrounding_building_to_radiance(building_geometry):
    building_name = building_geometry.name
    building_surfaces = []

    # walls
    for num, occ_face in enumerate(building_geometry.walls):
        surface_name = "surrounding_buildings_wall_{building_name}_{num}".format(building_name=building_name, num=num)
        building_surfaces.append(RadSurface(surface_name, occ_face, "reflectance0.2"))

    # roofs
    for num, occ_face in enumerate(building_geometry.roofs):
        surface_name = "surrounding_buildings_roof_{building_name}_{num}".format(building_name=building_name, num=num)
        building_surfaces.append(RadSurface(surface_name, occ_face, "reflectance0.2"))

    return building_surfaces


def create_rad_geometry(file_path, geometry_terrain, building_surface_properties, zone_building_names,
                        surroundings_building_names, geometry_pickle_dir):

    with open(file_path, "w") as rad_file:

        for terrain_surface in terrain_to_radiance(geometry_terrain):
            rad_file.write(terrain_surface.rad())

        for building_name in zone_building_names:
            building_geometry = BuildingGeometry.load(os.path.join(geometry_pickle_dir, 'zone', building_name))
            for building_surface in zone_building_to_radiance(building_geometry, building_surface_properties):
                rad_file.write(building_surface.rad())

        for building_name in surroundings_building_names:
            building_geometry = BuildingGeometry.load(os.path.join(geometry_pickle_dir, 'surroundings', building_name))
            for building_surface in surrounding_building_to_radiance(building_geometry):
                rad_file.write(building_surface.rad())
