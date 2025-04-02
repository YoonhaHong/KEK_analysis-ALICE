#!/usr/bin/env python3.9

import sys, argparse
from rich import print
from tqdm import tqdm
from utils.testbeam_QA_utils import *
from utils.testbeam_QA_plotting import *

import ROOT
#ROOT.gROOT.SetBatch(True)

def get_arguments():
    parser=argparse.ArgumentParser(description='The mighty testbeam data QA tool.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inputfile',  '-i', type=str, help='Raw-data-file to QA.')
    parser.add_argument('--localdir',  '-d', type=str, help='Directory that contains the raw-data-files.')
    parser.add_argument('--outputdir',  '-o', type=str, default='./plots/QA_babyMOSS', help='Output directory.')
    parser.add_argument('--corry',  '-e', type=str, default='/home/npl/Software/install/corryvreckan/bin/corry', help='corry executable.')
    parser.add_argument('--config',  '-c', type=str, default='./configs/testbeam_QA.conf', help='corry-config-file to run QA.')
    parser.add_argument('--geometry',  '-g', type=str, default='./geometry/tb2.conf', help='corry-geometry-file to run QA.')
    parser.add_argument('--plotting',  '-p', action='store_true', help='Only perform the plotting step.')
    parser.add_argument('--ow',  '-ow', default=True, action='store_true', help='Overwrite already existing QA files.')
    args=parser.parse_args()
    if not args.localdir and not args.inputfile:
        raise ValueError('No input file or input directory given.')
    if args.localdir and args.inputfile:
        raise ValueError('Only input file or input directory should be given.')
    return args

####################################################################################################
# MAIN
####################################################################################################

if __name__=="__main__":
    # get arguments
    args=get_arguments()
    raw_files = []

    if args.localdir is not None:
        if not args.localdir.endswith('/'): args.localdir+='/'

        # get available raw files to process
        print('Searching for raw-data-files ...')
        raw_files=find_files(args.localdir, ".raw")
    elif args.inputfile is not None:
        raw_files.append(os.path.abspath(args.inputfile))

    raw_no=len(raw_files)
    failed_runs=[]
    print('Found ',raw_no,' raw-data-files to evaluate.')

    # create corry mask files and get all other configuration parameters
    geometry_file=os.path.abspath(args.geometry)
    print('Found geometry file:\n', geometry_file)

    for f in tqdm(raw_files,desc="Processing raw-data-file"):
        # update config file with the right run
        run=get_run(f)
        header = os.path.basename(args.geometry)[:-5]
        filename =  header + '_' + 'QA_analysed_'+run+'.root'
        corry_output_file = os.path.join( os.path.abspath(args.outputdir), filename )
        if update_corry_config(args.config,f,corry_output_file)==0:
            # check if QA file already exists
            qa_done=os.path.exists(corry_output_file)

            # run corryvreckan
            status='0'
            if not args.plotting:
                if (qa_done and args.ow) or (not qa_done):
                    corry=args.corry+' -c '+os.path.abspath(args.config)+' -o detectors_file='+geometry_file
                    print("Running corryvreckan for run ",run," as:\n",corry)
                    status=run_shell_command(corry)
            if not status[0]=='0':
                print('Error while running corryvreckan.')
                failed_runs.append(f)
            else:
                print('Successfully processed raw-file.')

                # plot QA results
                print('Extract QA plots.')
                plot_QA_results(corry_output_file, os.path.abspath(args.outputdir),f+' with '+os.path.basename(args.geometry))
        else:
            print('Error while updating corryvreckan configuration.')
            failed_runs.append(f)

    # summary
    print("Finished testbeam data QA.")
    print('Processed ',raw_no,' raw-data-files.')
    print('QA failed for ',len(failed_runs),' runs:')
    for run in failed_runs:
        print(run)
    print("Results written to '"+args.outputdir+"'")

    sys.exit(0)
