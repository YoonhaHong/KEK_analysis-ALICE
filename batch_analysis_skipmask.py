#!/usr/bin/env python3.9

# batch analysis version of run_analysis_modify_conf.py
import pandas as pd
import os
import shutil
import argparse
import subprocess
import configparser
from tqdm import tqdm
from utils.run_corry import run_corry

MAX_EV = 60000

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated corryvreckan for batch analysis")
    parser.add_argument("csv_file_dir", type=str, help="Path to csv file to batch analyze")
    parser.add_argument("--raw_dir", '-o', type=str, default="../../cernbox/202503_KEK/data", help="Path to csv file to batch analyze")


    args = parser.parse_args()
    df = pd.read_csv( args.csv_file_dir )
    print(df)
    batch_name = os.path.basename( args.csv_file_dir )[:-4]

    print( f"batch analysis named {batch_name} started!\n\n")
    if not os.path.exists(f"./run/{batch_name}"):
        os.makedirs(f"./run/{batch_name}")
    else:
        shutil.rmtree(f"./run/{batch_name}") 

    if not os.path.exists(f"./output/{batch_name}"):
        os.makedirs(f"./output/{batch_name}")
    else:
        shutil.rmtree(f"./output/{batch_name}") 

    aligned_conf = ""
    regions = df.groupby("geometry")

    # 각 geometry 그룹에 대해 처리
    for region, group in tqdm(regions, ascii=True, desc="Processing geometries"):
        aligned_conf = ""

        for _, row in tqdm(group.iterrows(), total=len(group), ascii=True, desc=f"Processing {region}", position=0):
            run = os.path.join(args.raw_dir, row['raw_file'])
            runno = os.path.basename(run)[:-4]
            geometry = row['geometry']
            vcasb = int( row['VCASB'] )
            description = row['description']
            brief_name = f"{geometry}_VCASB{vcasb}"

            if "align" in description:
                print( "******************************")
                print( f"STARTING prealign, align of {region} : using {runno}" )
                print( "******************************\n")


                det_file_dir = os.path.abspath(f"./run/{batch_name}/{region}/")
                if os.path.exists(det_file_dir):
                    shutil.rmtree(det_file_dir)
                os.makedirs(det_file_dir)

                output_dir = f"./output/{batch_name}/{region}"
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
                os.makedirs(output_dir)

                #masked_conf =       run_corry(run = run, stage = "createmask",  det_file_dir = det_file_dir, detectors_file = f"./geometry/{region}.conf")
                prealigned_conf =   run_corry(run = run, stage = "prealign",    det_file_dir = det_file_dir, detectors_file = f"./geometry/{region}.conf")
                aligned_conf =      run_corry(run = run, stage = "align",       det_file_dir = det_file_dir, detectors_file = prealigned_conf)
                
                print( "******************************")
                print( f"aligned_conf : {aligned_conf}" )
                print( "******************************\n")  

            print( f"STARTING analysis of {runno} : {brief_name}" )
            run_corry(run = run, stage = "analyse", det_file_dir = det_file_dir, nevents=-1,     detectors_file = aligned_conf, output_dir=output_dir)
            
            # Rename the root file with brief_name
            root_file = os.path.join(output_dir, f"analyse_{runno}.root")
            if os.path.exists(root_file):
                new_name = os.path.join(output_dir, f"{brief_name}_{runno}.root")
                os.rename(root_file, new_name)
