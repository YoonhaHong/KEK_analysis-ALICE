import os
import shutil
import argparse
import subprocess
import configparser
import platform

if platform.system() == "Darwin":  # macOS
    CORRY = "/Users/yoonha/ITS3/corryvreckan/bin/corry"
else:  # Linux 
    CORRY = "/home/yoonha/ITS3/corryvreckan/bin/corry"

def modify_conf(base_conf, new_conf, updates):
    # ConfigParser 설정
    config = configparser.ConfigParser(allow_no_value=True, delimiters=("=", ":"))
    config.optionxform = str  # 대소문자 구분

    # base_conf 읽기
    config.read(base_conf)

    # updates 딕셔너리를 기반으로 설정값 수정
    for section, options in updates.items():
        if section not in config:
            config.add_section(section)
        for key, value in options.items():
            config.set(section, key, value)

    # 새로운 파일에 수정된 설정을 저장
    with open(new_conf, "w") as f:
        config.write(f, space_around_delimiters=False)
    
    # flush() 호출 후 파일을 닫아야 변경사항이 저장됨
    #f.flush()
    f.close()


def run_corry(**kwargs):
    # 필수 매개변수 확인
    required_params = ["run", "stage", "detectors_file"]
    for param in required_params:
        if param not in kwargs:
            raise ValueError(f"Missing required parameter: {param}")

    # 변수 추출 (기본값 설정)
    run = kwargs["run"]
    runno = os.path.basename(run)[:-4]

    momentum = kwargs.get("momentum", 5.0)  
    nevents = kwargs.get("nevents", 30000)  
    stage = kwargs["stage"]
    config = kwargs.get("config", f"./configs/1MOSS6ALPIDE/{stage}.conf" )
    output_dir = kwargs.get("output_dir", None) 
    det_file_dir = kwargs.get("det_file_dir", os.path.abspath(f"./run/{runno}") )
    detectors_file_path = os.path.abspath(kwargs["detectors_file"])
    
    result_path = os.path.join(det_file_dir, f"{stage}_{runno}.conf")


    # 업데이트할 설정
    updates = {
        "EventLoaderEUDAQ2": {
            "file_name": os.path.abspath(run)
        },
        "Corryvreckan": {
            "detectors_file": detectors_file_path,
            "detectors_file_updated": result_path,
            "number_of_events": str(nevents),
        }
    }

    if output_dir is not None:
        updates["Corryvreckan"]["histogram_file"] = os.path.join('..', output_dir, f"{stage}_{runno}.root")

    if stage in ["align", "analyse"]:
        updates["Tracking4D"] = {"momentum": f"{momentum}GeV"}
    if stage=="prealign" and momentum > 4.9:
        updates |= {"Prealignment": {"fit_range_rel": "50"}}
    #KEK beam is good at 5GeV/c

    new_conf = os.path.join(det_file_dir, f"{stage}.conf")

    modify_conf(config, new_conf, updates)

    # corry 실행
    cmd = [CORRY, "-c", new_conf]
    subprocess.run(cmd)

    # "analyse" 단계일 때 결과 파일 반환
    if stage == "analyse":
        return f"{stage}_{runno}.root"
    return result_path
