import os
import shutil
import argparse
import subprocess

MAX_EV = 6000

CORRY = "/Users/yoonha/ITS3/corryvreckan/bin/corry"

def run_corry(run, momentum, stage, det_file_dir, detectors_file):
    runno = os.path.basename(run)[:-4]
    result_path = os.path.join(det_file_dir, f"{stage}_{runno}.conf")
    config_path = f"./configs/2MOSS6ALPIDE_jhg/{stage}.conf"
    
    cmd = [
        CORRY,
        "-c", config_path,
        "-o", f"EventLoaderEUDAQ2.file_name = {os.path.abspath(run)}",
        "-o", f"detectors_file = {args.geometry if stage=="createmask" else
                                  os.path.join(det_file_dir, detectors_file)}",
        "-o", f"detectors_file_updated = {result_path}",
        "-o", f"number_of_events = {MAX_EV}",        
        "-o", f"histogram_file = {stage}.root",
    ]
    
    if stage == "align" or "analyse":
        cmd.append("-o")
        cmd.append(f"momentum={momentum}GeV")
    
    subprocess.run(cmd)
    return result_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated corryvreckan")
    parser.add_argument('raw_file_dir', type=str, 
                        help="Path to raw file to analyze")
    parser.add_argument('-p', '--beam_momentum', type=float, default=3.0, 
                        help='Beam momentum, default 3.0 GeV/c')
    parser.add_argument('-g', '--geometry', type=str, default="/Users/yoonha/ITS3/202412KEK_analysis/geometry/2MOSS6ALPIDE.conf",
                        help="Path to geometry file")

    
    args = parser.parse_args()

    run = args.raw_file_dir
    runno=os.path.basename(run)[:-4]
    momentum = args.beam_momentum

    det_file_dir = os.path.abspath(f"./run/{runno}")
    if os.path.exists(det_file_dir):
        shutil.rmtree(det_file_dir)
    os.makedirs(det_file_dir)

    masked_conf = run_corry(run, momentum, "createmask", det_file_dir, '')
    prealigned_conf = run_corry(run, momentum, "prealign", det_file_dir, masked_conf)
    aligned_conf = run_corry(run, momentum, "align", det_file_dir, prealigned_conf)
    run_corry(run, momentum, "analyse",det_file_dir, aligned_conf)

    


