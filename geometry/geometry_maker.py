#!/usr/bin/env python3.9

import os
from math import sqrt
import pandas as pd
from configparser import ConfigParser

dict_hu_info =[
    {"hu": "top", "posy": 0, "npixels": 256, "pixel_pitch_um":22.5, "orientation" : "0deg, 180deg, 0deg"},
    {"hu": "bot", "posy": 0, "npixels": 320, "pixel_pitch_um":18.0, "orientation" : "0deg, 0deg, 180deg"}    
]
material_budget = 0.0005

moss_index = 3
moss_posz_mm  = 75
moss_posy_mm  = 0
dict_reg_info =[
    {"reg": "tb0", "posx_mm": 10,   "roi": "[[32,0],[32,160],[256,160],[256,0]]"},
    {"reg": "tb1", "posx_mm": 4,    "roi": "[[0,0],[0,160],[256,160],[256,0]]"},
    {"reg": "tb2", "posx_mm": -2,   "roi": "[[0,0],[0,160],[256,160],[256,0]]"},
    {"reg": "tb3", "posx_mm": -8,   "roi": "[[0,0],[0,160],[224,160],[224,0]]"},
    {"reg": "bb0", "posx_mm": 10,   "roi": "[[40,0],[40,200],[320,200],[320,0]]"},
    {"reg": "bb1", "posx_mm": 4,    "roi": "[[0,0],[0,200],[320,200],[320,0]]"},
    {"reg": "bb2", "posx_mm": -2,   "roi": "[[0,0],[0,200],[320,200],[320,0]]"},
    {"reg": "bb3", "posx_mm": -8,   "roi": "[[0,0],[0,200],[280,200],[280,0]]"},
]




def create_geometry_conf(base_conf, reg, output_dir="."):
    """
    Create geometry file according to 'base_conf'

    :param base_conf: path of template .conf file(str)
    :param reg: region name (str)(ex: tb1)
    :param roi: ROI (str)(ex: [[100, 0], [100, 200], [320, 200], [320, 0]])
    :param material_budget: material_budget (float)(ex: 0.0005)
    :param output_dir: directory to save created geometry file (default: ".")
    """
    # path to save
    output_file = os.path.join(output_dir, f"{reg}.conf")
    dut_name = f"{reg[0:2]}_reg{reg[-1]}_{moss_index}"
    hu = ""
    if reg[0:2] == "tb":
        hu = "top"
    elif reg[0:2] == "bb":
        hu = "bot"
    else:
        ValueError("Not a valid region name")


    hu_info = pd.DataFrame(dict_hu_info)
    npixels = hu_info[hu_info["hu"]==hu]["npixels"].values[0]
    pixel_pitch_um = hu_info[hu_info["hu"]==hu]["pixel_pitch_um"].values[0]
    spatial_resolution_um = pixel_pitch_um/sqrt(12)
    orientation = hu_info[hu_info["hu"]==hu]["orientation"].values[0]

    reg_info = pd.DataFrame(dict_reg_info)
    posx_mm = reg_info[reg_info["reg"]==reg]["posx_mm"].values[0]
    roi = reg_info[reg_info["reg"]==reg]["roi"].values[0] 

    config = ConfigParser()
    config.read(base_conf)

    # add new section
    new_section = f"{dut_name}"
    config[new_section] = {
        'type': '"MOSS"',
        'position': f'{posx_mm}mm,{moss_posy_mm}mm,{moss_posz_mm}mm',
        'number_of_pixels': f'{npixels},{npixels}',
        'pixel_pitch': f'{pixel_pitch_um:.1f}um, {pixel_pitch_um:.1f}um',
        'spatial_resolution': f'{spatial_resolution_um:.1f}um, {spatial_resolution_um:.1f}um',
        'time_resolution': '10s',
        'material_budget': str(material_budget),
        'coordinates': '"cartesian"',
        'orientation': f'{orientation}',
        'orientation_mode': 'xyz',
        'role': '"DUT"',
        'roi': f'{roi}',
    }

    # save new config
    with open(output_file, "w") as file:
        config.write(file)

    print(f"Created {output_file}")


if __name__ == "__main__":
    # get region name at console
    reg = input("Enter region name (e.g., tb1): ")
    #  
    base_conf = "6ALPIDE.conf"

    create_geometry_conf(base_conf, reg)