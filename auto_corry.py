import os
import argparse
import subprocess

CORRY = "/Users/yoonha/ITS3/corryvreckan/bin/corry"
MAX_EV = 6000 

def createmask(run):
    runno = os.path.basename(run)[:-4]
    outconf = f"../../geometry/masked_{runno}.conf"
    cmd = [
    CORRY, 
        "-c", "./configs/2MOSS6ALPIDE/createmask.conf",
        "-o", "detectors_file = ../../geometry/2MOSS6ALPIDE.conf",
        "-o", f"detectors_file_updated = ../../geometry/masked_{runno}.conf",
        "-o", f"number_of_events = {MAX_EV}",
        "-o", f"file_name = {run}" 
    ]
    subprocess.run(cmd)
    return outconf

def prealign(run, inconf):
    runno = os.path.basename(run)[:-4]
    outconf = f"../../geometry/prealigned_{runno}.conf"
    cmd = [
    CORRY, 
        "-c", "./configs/2MOSS6ALPIDE/prealign.conf",
        "-o", f"detectors_file = {inconf}",
        "-o", f"detectors_file_updated = ../../geometry/prealigned_{runno}.conf",
        "-o", f"number_of_events = {MAX_EV}",
        "-o", f"file_name = {run}" 
    ]
    subprocess.run(cmd)
    return outconf

def align(run, inconf, momentum):
    runno = os.path.basename(run)[:-4]
    outconf = f"../../geometry/aligned_{runno}.conf"
    cmd = [
    CORRY, 
        "-c", "./configs/2MOSS6ALPIDE/align.conf",
        "-o", f"detectors_file = {inconf}",
        "-o", f"detectors_file_updated = ../../geometry/aligned_{runno}.conf",
        "-o", f"number_of_events = {MAX_EV}",
        "-o", f"file_name = {run}",
        "-o", f"momentum={momentum}"
    ]
    subprocess.run(cmd)
    return outconf

def analyse(run, inconf, momentum):
    runno = os.path.basename(run)[:-4]
    cmd = [
    CORRY, 
        "-c", "./configs/2MOSS6ALPIDE/analyse.conf",
        "-o", f"detectors_file = {inconf}",
        "-o", f"number_of_events = {MAX_EV}",
        "-o", f"momentum={momentum}" 
        "-o", f"histogram_file = analysis_{runno}.conf",
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated corryvreckan")
    parser.add_argument('raw_file_dir', type=str, help="Path to raw file to analyze")

    parser.add_argument('-p', '--beam_momentum', type=float, default=3.,
                        help='beam momentum, default 3.0 GeV/c')

    args = parser.parse_args()
    run_m = args.raw_file_dir

    masked_conf = createmask(run_m)
    prealigned_conf = prealign(run_m, masked_conf )
    aligned_conf = align(run_m, prealigned_conf, args.beam_momentum)
    analyse(run_m, aligned_conf, args.beam_momentum)

    


