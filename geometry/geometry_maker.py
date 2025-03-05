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
moss_posz_mm  = 76.2
moss_posy_mm  = 0
dict_reg_info =[
    {"reg": "tb0", "posx_mm": 8,    "roi": None},
    {"reg": "tb1", "posx_mm": 2,    "roi": None},
    {"reg": "tb2", "posx_mm": -4,   "roi": None},
    {"reg": "tb3", "posx_mm": -10,  "roi": None},
    {"reg": "bb0", "posx_mm": 10,   "roi": None},
    {"reg": "bb1", "posx_mm": 4,    "roi": None},
    {"reg": "bb2", "posx_mm": -2,   "roi": None},
    {"reg": "bb3", "posx_mm": -8,   "roi": None},
]




def create_geometry_conf(base_conf, reg, output_dir="."):
    """
    base_conf를 기반으로 새로운 geometry 설정 파일을 생성합니다.

    :param base_conf: 기본 설정 파일 경로 (예: 6ALPIDE.conf)
    :param reg: 생성할 region 이름 (예: tb1)
    :param roi: ROI 값 (리스트 형태, 예: [[100, 0], [100, 200], [320, 200], [320, 0]])
    :param material_budget: material_budget 값 (예: 0.0005)
    :param output_dir: 출력 디렉토리 (기본값: 현재 디렉토리)
    """
    # 출력 파일 경로
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

    # 새로운 섹션 추가
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
        'role': '"DUT"'
    }
    if roi is not None: config[new_section] |= {'roi': roi}

    # 새로운 설정 파일 저장
    with open(output_file, "w") as file:
        config.write(file)

    print(f"Created {output_file}")


if __name__ == "__main__":
    # 사용자 입력 받기
    reg = input("Enter region name (e.g., tb1): ")
    # 기본 설정 파일 경로
    base_conf = "6ALPIDE.conf"

    # 설정 파일 생성
    create_geometry_conf(base_conf, reg)