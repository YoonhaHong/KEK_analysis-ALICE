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

def run_corry(run, momentum, nevents, stage, det_file_dir, detectors_file, output_dir):
    runno = os.path.basename(run)[:-4]
    result_path = os.path.join(det_file_dir, f"{stage}_{runno}.conf")

    detectors_file_path = os.path.abspath( detectors_file )

    updates = {
        "EventLoaderEUDAQ2": {
            "file_name": os.path.abspath(run)
        },
        "Corryvreckan": {  
            "detectors_file": detectors_file_path, 
            "detectors_file_updated": result_path,
            "number_of_events": str(nevents),
        },

    }
    #if stage=="align" and momentum == 5.0:
    #    updates["Prealignment"]["fit_range_rel"] = 50
    #KEK beam is good at 5GeV/c

    if stage == "analyse" or stage == "prealign":
        updates["Corryvreckan"]["histogram_file"] = f"{output_dir}/{stage}_{runno}.root"
    #else:
    #    updates["Corryvreckan"]["histogram_file"] = f"{output_dir}/{stage}.root"


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
    parser.add_argument("-n", "--nevents", type=int, default=30000, help="Number of events to analyze set -1 to analyze all events, default = 30000")

    args = parser.parse_args()

    run = args.raw_file_dir
    runno = os.path.basename(run)[:-4]
    momentum = args.beam_momentum

    print( f"batch analysis named babyMOSS started!\n\n")
    if not os.path.exists(f"./run/babyMOSS/{runno}"):
        os.makedirs(f"./run/babyMOSS/{runno}")
    else:
        shutil.rmtree(f"./run/babyMOSS/{runno}") 

    if not os.path.exists(f"./output/babyMOSS/{runno}"):
        os.makedirs(f"./output/babyMOSS/{runno}")
    else:
        shutil.rmtree(f"./output/babyMOSS/{runno}") 
    
    geofiles = ["./geometry/tb1.conf",
                "./geometry/tb2.conf",
                "./geometry/bb1.conf",
                "./geometry/bb2.conf",]
    
    for det in geofiles:
        det_name = os.path.basename(det)[:-5]
        print( "******************************")
        print( det_name )
        print( "******************************\n")
        os.makedirs(f"./output/babyMOSS/{runno}/{det_name}")


        det_file_dir = os.path.abspath(f"./run/babyMOSS/{det_name}/")
        if os.path.exists(det_file_dir):
            shutil.rmtree(det_file_dir)
        os.makedirs(det_file_dir)

        output_dir = f"./output/babyMOSS/{runno}/{det_name}"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    # 각 단계 실행
        masked_conf = run_corry(run, momentum, 30000, "createmask", det_file_dir, det, 
                                            output_dir="."+output_dir)

        prealigned_conf = run_corry(run, momentum, 30000, "prealign", det_file_dir, masked_conf,
                                            output_dir="."+output_dir )

        aligned_conf = run_corry(run, momentum, 30000, "align", det_file_dir, prealigned_conf,
                                            output_dir="."+output_dir )
        run_corry(run, momentum, args.nevents, "analyse", det_file_dir, aligned_conf,
                                            output_dir="."+output_dir )
