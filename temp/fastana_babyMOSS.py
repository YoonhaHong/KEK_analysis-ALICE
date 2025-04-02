#!/usr/bin/env python3.9

import sys, argparse
import shutil
from rich import print
from tqdm import tqdm
from utils.testbeam_QA_utils import *
from utils.testbeam_QA_plotting import *
from utils.QA_beamstr_plotting import plot_beamstr
from utils.run_corry import run_corry

import ROOT
#ROOT.gROOT.SetBatch(True)

def get_arguments():
    parser=argparse.ArgumentParser(description='QA tool for KEK beam str', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inputfile', '-i', type=str, help='Raw-data-file to QA.')
    parser.add_argument('--outputdir',  '-o', type=str, default='./plots/QA_beamstr/', help='Output directory.')
    parser.add_argument('--nevents',  '-n', type=int, default=30000, help='# of events.')
    parser.add_argument('--corry',  '-e', type=str, default='/home/npl/Software/install/corryvreckan/bin/corry', help='corry executable.')
    parser.add_argument('--momentum', '-P', type=float, default=5.0, help="Beam momentum, default 5.0 GeV/c")
    parser.add_argument('--geometry',  '-g', type=str, default='./geometry/tb0.conf', help='corry-geometry-file to run QA.')
    parser.add_argument('--plotting',  '-p', action='store_true', help='Only perform the plotting step.')
    parser.add_argument('--ow',  '-ow', action='store_true', help='Overwrite already existing QA files.')
    args=parser.parse_args()
    return args

####################################################################################################
# MAIN
####################################################################################################

if __name__=="__main__":

    args=get_arguments()
    run = args.inputfile
    runno = os.path.basename(run)[:-4]
    momentum = args.momentum

    det_file_dir = os.path.abspath(f"./run/{runno}")
    if os.path.exists(det_file_dir):
        shutil.rmtree(det_file_dir)
    os.makedirs(det_file_dir)

    root_file_dir = '.'+args.outputdir
    if not args.plotting:
        masked_conf =       run_corry(run = run, stage = "createmask", detectors_file = args.geometry)
        prealigned_conf =   run_corry(run = run, stage = "prealign",   detectors_file = masked_conf)
        aligned_conf =      run_corry(run = run, stage = "align",      detectors_file = prealigned_conf)
        root_file_name =    run_corry(run = run, stage = "analyse",    nevents=args.nevents,   detectors_file = aligned_conf, output_dir=args.outputdir)
    
    else:
        root_file_name =    f"analyse_{runno}.root"

    if not os.path.exists(args.outputdir): os.mkdir(args.outputdir)
