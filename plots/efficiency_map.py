import sys
import os
import ROOT
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import argparse
from datetime import date, datetime
from drawing import *



    

#if __name__ == "__main__":
    # Base directory containing batch_analysis folders
parser = argparse.ArgumentParser()
parser.add_argument("base_dir", type=str)
parser.add_argument("-o", "--output_dir", type=str, required=False, default=".")
parser.add_argument("-v", "--vcasb", type=int, required=False, default=91)
parser.add_argument("-r", "--rebin", type=int, required=False, default=4)

args = parser.parse_args()
base_directory = args.base_dir[:-1] if args.base_dir.endswith("/") else args.base_dir # delete "/"
output_dir = os.path.join(args.output_dir, os.path.basename(base_directory))

title = ROOT.TPaveLabel(0.1, 0.90, 0.9, 0.99, f"{os.path.basename(base_directory)}, VCASB = {args.vcasb}")
title.SetFillColor(0)  # 투명 배경
title.SetBorderSize(0)  # 테두리 없음

eff_local_canvas = ROOT.TCanvas("eff_local", "", 1200, 300)
eff_local_canvas.Divide(4, 1, 0.01, 0.01)
eff_local_canvas.cd()
title.Draw()

eff_global_canvas = ROOT.TCanvas("eff_global", "", 1200, 300)
eff_global_canvas.Divide(4, 1, 0.01, 0.01)
eff_global_canvas.cd()
title.Draw()

#ROOT.gStyle.SetPalette( ROOT.kTemperatureMap)
ROOT.gStyle.SetOptStat(0)

for detector in os.listdir(base_directory):
    detector_path = os.path.join(base_directory, detector)
    if not os.path.isdir(detector_path):
        continue

    dut_name = detector[0:2] + "_reg" + detector[2] + "_3"
    
    for file in os.listdir(detector_path):
        if file.endswith(".root"):
            root_file_path = os.path.join(detector_path, file)
            match = re.search(r'VCASB(\d+)', file)
            VCASB = int(match.group(1)) if match else 1
        if VCASB == args.vcasb: break

    root_file = ROOT.TFile.Open(root_file_path)
    if not root_file or root_file.IsZombie():
        print(f"failed to open: {root_file_path}")
        continue

    eff_local_path = f"AnalysisEfficiency/{dut_name}/chipEfficiencyMap_trackPos_TProfile"
    eff_local_hist = root_file.Get(eff_local_path)
    #if not isinstance(eff_local_hist, ROOT.TH1) and not isinstance(eff_local_hist, ROOT.TH2): continue
    eff_local_hist.SetName(f"{detector[0:3]}")
    eff_local_hist.SetTitle("")
    eff_local_canvas.cd( int(detector[2])+1 )
    eff_local_hist.SetMinimum(0)
    eff_local_hist.SetMaximum(1)
    eff_local_hist.Rebin2D(args.rebin, args.rebin)
    eff_local_hist.DrawCopy("COLZ")

    eff_global_path = f"AnalysisEfficiency/{dut_name}/pixelEfficiencyMap_trackPos_TProfile"
    eff_global_hist = root_file.Get(eff_global_path)
    #if not isinstance(eff_global_hist, ROOT.TH1) and not isinstance(eff_global_hist, ROOT.TH2): continue
    eff_global_hist.SetName(f"{detector[0:3]}")
    eff_global_hist.SetTitle("")
    eff_global_canvas.cd( int(detector[2])+1 )
    eff_global_hist.SetMinimum(0)
    eff_global_hist.SetMaximum(1)
    eff_global_hist.DrawCopy("COLZ")

eff_local_canvas.Update()
eff_local_canvas.SaveAs(f"{output_dir}/{os.path.basename(base_directory)}, VCASB={args.vcasb} effmap(local)_r{args.rebin}.pdf")

eff_global_canvas.Update()
eff_global_canvas.SaveAs(f"{output_dir}/{os.path.basename(base_directory)}, VCASB={args.vcasb} effmap(global).pdf")

        




