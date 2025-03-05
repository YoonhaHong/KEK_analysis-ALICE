import os
import shutil
import argparse
import subprocess
import configparser

MAX_EV = 60000
CORRY = "/Users/yoonha/ITS3/corryvreckan/bin/corry"

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

def run_corry(run, momentum, nevents, stage, det_file_dir, detectors_file):
    runno = os.path.basename(run)[:-4]
    result_path = os.path.join(det_file_dir, f"{stage}_{runno}.conf")

    _detectors_file_path = args.geometry if stage == "createmask" else detectors_file
    detectors_file_path = os.path.abspath( _detectors_file_path )

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

    #if stage == "align":
    # if stage == "analyse" or stage == "prealign":
    #else:
    #    updates["Corryvreckan"]["histogram_file"] = f"{stage}.root"
    updates["Corryvreckan"]["histogram_file"] = f"./momentum_scan/{int(args.beam_momentum)}GeVc/{stage}_{runno}.root"


# "align"과 "analyse"일 때 momentum 추가
    if stage in ["align", "analyse"]:
        updates["Tracking4D"] = {"momentum": f"{momentum}GeV"}


    # conf 파일 수정
    old_conf = f"./configs/2MOSS6ALPIDE/{stage}.conf"
    new_conf = os.path.join(det_file_dir, f"{stage}.conf")

    modify_conf(old_conf, new_conf, updates)

    # corry 실행
    cmd = [CORRY, "-c", new_conf]
    subprocess.run(cmd)

    return result_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated corryvreckan")
    parser.add_argument("raw_file_dir", type=str, help="Path to raw file to analyze")
    parser.add_argument("-p", "--beam_momentum", type=float, default=3.0, help="Beam momentum, default 3.0 GeV/c")
    parser.add_argument("-g", "--geometry", type=str, 
                         default="/Users/yoonha/ITS3/202412KEK_analysis/geometry/6ALPIDE.conf",
                         #default="/Users/yoonha/ITS3/202412KEK_analysis/geometry/test.conf",
                        help="Path to geometry file")

    args = parser.parse_args()

    run = args.raw_file_dir
    runno = os.path.basename(run)[:-4]
    momentum = args.beam_momentum

    det_file_dir = os.path.abspath(f"./run/{runno}")
    if os.path.exists(det_file_dir):
        shutil.rmtree(det_file_dir)
    os.makedirs(det_file_dir)

    # 각 단계 실행
    masked_conf = run_corry(run, momentum, 30000, "createmask", det_file_dir, '')
    prealigned_conf = run_corry(run, momentum, 30000, "prealign", det_file_dir, masked_conf)
    aligned_conf = run_corry(run, momentum, 30000, "align", det_file_dir, prealigned_conf)
    run_corry(run, momentum, -1, "analyse", det_file_dir, aligned_conf)