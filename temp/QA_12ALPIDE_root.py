import sys, argparse
from utils.testbeam_QA_plotting import *

import ROOT
#ROOT.gROOT.SetBatch(True)

def get_arguments():
    parser=argparse.ArgumentParser(description='The mighty testbeam data QA tool.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inputfile',  '-i', type=str, help='Raw-data-file to QA.')
    parser.add_argument('--localdir',  '-d', type=str, help='Directory that contains the raw-data-files.')
    parser.add_argument('--outputdir',  '-o', type=str, default='./plots/QA_12ALPIDE', help='Output directory.')
    parser.add_argument('--corry',  '-e', type=str, default='/home/npl/Software/install/corryvreckan/bin/corry', help='corry executable.')
    parser.add_argument('--config',  '-c', type=str, default='./configs/testbeam_QA.conf', help='corry-config-file to run QA.')
    parser.add_argument('--geometry',  '-g', type=str, default='./geometry/12ALPIDE.conf', help='corry-geometry-file to run QA.')
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
    plot_QA_results_12ALPIDE(args.inputfile, args.outputdir, "test")
