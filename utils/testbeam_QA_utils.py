#!/usr/bin/env python3

import os
import sys
import glob
import subprocess
from datetime import datetime
import tempfile
import pandas as pd
from rich import print

def create_csv_file(directory, file_name):
    # check outputfolder for csv output_name
    print("Checking for '"+file_name+"' in: \n"+directory)
    for file in glob.glob(directory+"/*"):
        file = os.path.basename(file)
        if file == file_name:
            print("Found existing .csv file. What do you want to do? q: quit, o: overrite, a: append. Answer:")
            answer = str(input())
            if answer=='q':
                print("Quitting program.")
                sys.exit(0)
            elif answer=='o':
                print("Overwriting existing file.")
                csv_file = open(directory + file_name, "w")
                print("Opened csv_file with path: \n"+directory+file_name)
                return 0,csv_file
            elif answer=='a':
                print("Adding to existing file.")
                csv_file = open(directory + file_name, "a")
                print("Opened csv_file with path: \n"+directory+file_name)
                return -1,csv_file
            else:
                print("Invalid answer. Quitting program.")
                sys.exit(0)
        else:
            continue
    csv_file = open(directory + file_name, "w")
    return 0,csv_file

def find_files(path:str, suffix:str):
    cand=[]
    if path[-1]!='/':
        path+='/'
    for filename in glob.iglob(path+'**/*'+suffix, recursive=True):
        cand.append(os.path.abspath(filename))
    return cand

def get_timestamp(r):
    if ".raw" in r: r=r.replace(".raw","")
    if "run" in r: r=r.replace("run","")
    time_stamps = r.split("_")
    if len(time_stamps)==2:
        time_stamp = time_stamps[1]
        if len(time_stamp) == 12:
            year = int(time_stamp[0:2])
            year += 2000
            month = int(time_stamp[2:4])
            day = int(time_stamp[4:6])
            hour = int(time_stamp[6:8])
            minute = int(time_stamp[8:10])
            second = int(time_stamp[10:])
            return datetime(year, month, day, hour, minute, second)
        else:
            print("Unexpected timestamp format: "+str(time_stamps[1]))
            return -1    
    else:
        return -1
        
def get_sorted_runs(runs_list):
    timestamps=[]
    runnames=[]
    for run in runs_list:
        r=os.path.basename(run)
        t=get_timestamp(r)
        if not t==-1:
            runnames.append(run) # r
            timestamps.append(t)
    return [run for _,run in sorted(zip(timestamps,runnames))]

def get_raw_head(file, depth = 30):
    trigger_words = ["Name"]
    # executing command to get first lines from raw file
    command = "head -"+str(depth)+" "+ file
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen([command], shell=True, stdout=tempf, stderr=subprocess.STDOUT)
        proc.wait()
        tempf.seek(0)
        # read the output tempfile
        lines = tempf.readlines()
        lines_dec = []
        for line in lines:
            line_dec = str(line)
            for trigger in trigger_words:
                if trigger in line_dec:
                    if line_dec in lines_dec: # avoid doubles
                        continue
                    else:
                        line_dec = line_dec.strip('b')
                        line_dec = line_dec.strip('\'')
                        line_dec = line_dec.strip('\n')
                        line_dec = line_dec.strip('\\n')
                        line_dec = line_dec.strip(' ')
                        lines_dec.append(line_dec)
                else:
                    continue
    return lines_dec

def get_eudaq2_detector_parameters(path, chip_id, triggers, verbose=False): # ALPIDE
    # needed paramters BackBiasVoltage,ITHR,VCASN,VCASN2,VCLIP,RunEventLimit,ConfigFile
    keys = []
    values = []
    if type(chip_id) is list:
        PRODl = ["Producer."+c for c in chip_id]
    else:
        PRODl = ["Producer."+chip_id]
    prod_found = False
    RC = "RunControl"
    rc_found = False
    with open(path, "r") as file:
        for i in file:
            line = str(i).strip()
            # remove comment
            idx = line.rfind("#")
            if idx != -1:
                line = line[:idx]
            if line == "":
                continue
                
            # get parameters of interest
            for PROD in PRODl:
                if PROD in line:
                    rc_found = False
                    prod_found = True
                if RC in line:
                    rc_found = True
                    prod_found = False
                elif "Producer." in line:
                    rc_found = False

            if rc_found and "NEVENTS" in line:
                idx = line.rfind("=")
                if idx != -1:
                    line = line[idx+1:]
                    line = line.replace(" ","")
                    keys.append("NEVENTS")
                    values.append(line)
            if prod_found:
                for tr in triggers:
                    oline=line
                    if tr in line or tr.upper() in line.upper():
                        idx = line.rfind("=")
                        if idx != -1:
                            line = line[idx+1:]
                            line = line.replace(" ","")
                        if "VOLTAGE" in tr.upper():
                            keys.append(tr)
                        elif "POS_DUT_ROT" in tr.upper():
                            keys.append(tr)
                        elif "IBIASN" in oline.upper():
                            keys.append("IBIASN")
                        elif "VCASB" in tr:
                            keys.append(tr)
                        elif "VSHIFT" in tr:
                            keys.append(tr)
                        elif "IRESET" in tr:
                            keys.append(tr)
                        else:
                            keys.append(tr.split("_")[-1])
                        if keys[-1]=="IBIAS":
                            values.append(str(float(line)*10))
                        else:
                            values.append(line)
                        if verbose:
                            print("TRIGGER: ",tr," KEY: ",keys[-1]," VALUE: ",values[-1]," LINE: ",oline)

    # create directory
    dict = {key:value for (key,value) in zip(keys,values)}
    return dict

def run_shell_command(command:str, trigger:str=""):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    prev_empty = False
    get_var = False
    trigs = []
    while process.poll() is None:
        output = process.stdout.readline()

        # decode output from byte class object
        line = str(output.decode("utf-8")).strip("\n")

        # supress subsequent empty lines
        if line == "" and not prev_empty:
            prev_empty = True
            print(line)
        elif line == "" and prev_empty:
            prev_empty = True
        else:
            prev_empty = False
            print(line)
            if not trigger == "":
                if str(trigger) in line and not get_var:
                    get_var = True
                elif get_var:
                    line = line.strip()
                    line = line.replace(" ","")
                    trigs.append(line)
                    get_var = False
            else:
                trigs.append("")
    exit_code = process.poll()
    trigs.insert(0,str(exit_code))
    return trigs

def get_run(path):
    idx=path.rfind("run")
    if idx==-1:
        return "000000000_000000000000"
    return path[idx+3:idx+25]

def get_dir(config_file):
    idx=config_file.rfind('/')
    if idx==-1:
        return os.path.abspath('./')
    return os.path.abspath(config_file[:idx])

def get_file(config_file):
    idx=config_file.rfind('/')
    if idx==-1:
        return ""
    return config_file[idx+1:]

def update_corry_config(config_file, run_file, output, geometry=""):
    # modify file
    modified_lines = 0
    data = []
    loader = False
    writer = False
    with open(config_file, 'r') as file:
        data = file.readlines()
        if len(data) == 0:
            print("Cannot read file content of: \n"+config_file)
            return 1
        else:
            for i in range(0, len(data)):
                line = str(data[i])
                #print("LINE:", line)
                if line.startswith('#'):
                    continue
                if "detectors_file" in line and geometry!="":
                    data[i] = "detectors_file = \""+geometry+"\"\n"
                    modified_lines += 1
                if "output_directory" in line:
                    data[i] = "output_directory = \""+get_dir(output)+"\"\n"
                    #data[i] = "output_directory = \""+(os.path.dirname(os.path.abspath(output))).as_posix()+"\"\n"
                    modified_lines += 1
                if "histogram_file" in line:
                    data[i] = "histogram_file = \""+get_file(output)+"\"\n"
                    #data[i] = "histogram_file = \""+(os.path.basename(output)).as_posix()+"\"\n"
                    modified_lines += 1
                if "Loader" in line:
                    loader = True
                if "file_name" in line and loader:
                    data[i] = "file_name = \""+run_file+"\"\n"
                    modified_lines += 1
                    loader = False
                if "Writer" in line:
                    writer = True
                if "file_name" in line and writer:
                    data[i] = "histogram_file = \""+output.replace(".root",".writer")+"\"\n"
                    modified_lines += 1
                    writer = False
                else:
                    continue

    with open(config_file, 'w') as file: # overwrite old file
        file.writelines(data)
    #print('Modified ',modified_lines,' lines.')
    return 0

def create_corry_masks(config_file, config_dir):
    detectors=[]
    masks=[]
    with open(config_file, 'r') as file:
        data = file.readlines()
        if len(data) == 0:
            print("Cannot read file content of: \n"+config_file)
            return 1
        else:
            for i in range(0, len(data)):
                line = str(data[i]).strip()
                #print(line)
                i1=line.find('[')
                i2=line.rfind(']')
                if i1!=-1 and i2!=-1:
                    detectors.append(line[i1+1:i2])
                elif "mask_file" in line and len(masks)<len(detectors):
                    i1=line.find('\"')
                    i2=line.rfind('\"')
                    if i1!=-1 and i2!=-1 and i1!=i2:
                        masks.append(os.path.abspath(line[i1+1:i2]))
                        data[i]="mask_file = \""+masks[-1]+"\"\n"
                else:
                    continue
    if not os.path.exists(config_dir+'/masks'):
        os.makedirs(config_dir+'/masks')
    for m in masks:
        status=run_shell_command("touch "+m)
        print("Created dummy mask file:\n"+m)
    with open(config_file, 'w') as file: # overwrite old file
        file.writelines(data)
    return 0