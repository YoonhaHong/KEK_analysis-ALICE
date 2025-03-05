#!/usr/bin/env python3

import os
import glob
import subprocess
from rich import print
#from testbeam_QA_utils import *

import ROOT
#ROOT.gROOT.SetBatch(True)

def plot_QA_results(corry_input,outputdir,name):
    fileRoot = ROOT.TFile.Open(corry_input,"READ")
    regions = ["tb_reg0_3", "tb_reg1_3", "tb_reg2_3", "tb_reg3_3", "bb_reg0_3", "bb_reg1_3", "bb_reg2_3", "bb_reg3_3"]
    regions_to_draw = []
    for region in regions:
        if hasattr(fileRoot.EventLoaderEUDAQ2, region): regions_to_draw.append(region)
    print("Detected regions: ", regions_to_draw)
    nregion = len(regions_to_draw)

    frac_dut = nregion*250 / (1000 + 250 * nregion)
    c1 = ROOT.TCanvas('c1', 'c1', 0, 0, 1000+250*nregion, 1000)
    #                                        x1,  y1,  x2,  y2)
    pad1 = ROOT.TPad("pad1","This is pad1",0.01,0.92,0.99,0.99)
    pad2 = ROOT.TPad("pad2","This is pad2",0.01,0.01,1-frac_dut-0.05,0.92)
    pad3 = ROOT.TPad("pad3","This is pad3",1-frac_dut,0.01,0.99,0.92)
    pad1.Draw()
    pad2.Draw()
    pad3.Draw()
    # print LABEL
    pad1.cd()
    title = ROOT.TLatex()
    title.SetTextSize(0.3)
    title.DrawLatex(.05,0.1,str(name))
    info = ROOT.TLatex()
    info.SetTextSize(0.3)
    infostr=""
    info.DrawLatex(.05,0.5,infostr)
    # gStyle options
    ROOT.gStyle.SetOptStat("emr")
    ROOT.gStyle.SetPadRightMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.10)
    ROOT.gStyle.SetPadTopMargin(0.09)
    ROOT.gStyle.SetPadBottomMargin(0.09)

    # print ALPIDE hitmaps
    pad2.cd()
    pad2.Divide(2,3)
    hitmapA0 = fileRoot.EventLoaderEUDAQ2.ALPIDE_0.Get("hitmap")
    hitmapA1 = fileRoot.EventLoaderEUDAQ2.ALPIDE_1.Get("hitmap")
    hitmapA2 = fileRoot.EventLoaderEUDAQ2.ALPIDE_2.Get("hitmap")
    hitmapA3 = fileRoot.EventLoaderEUDAQ2.ALPIDE_5.Get("hitmap")
    hitmapA4 = fileRoot.EventLoaderEUDAQ2.ALPIDE_6.Get("hitmap")
    hitmapA5 = fileRoot.EventLoaderEUDAQ2.ALPIDE_7.Get("hitmap")
    hitmapA0.SetTitle("Hitmap ALPIDE_0")
    hitmapA1.SetTitle("Hitmap ALPIDE_1")
    hitmapA2.SetTitle("Hitmap ALPIDE_2")
    hitmapA3.SetTitle("Hitmap ALPIDE_5")
    hitmapA4.SetTitle("Hitmap ALPIDE_6")
    hitmapA5.SetTitle("Hitmap ALPIDE_7")
    pad2.cd(1)
    hitmapA0.Draw("COLZ")
    pad2.cd(2)
    hitmapA1.Draw("COLZ")
    pad2.cd(3)
    hitmapA2.Draw("COLZ")
    pad2.cd(4)
    hitmapA3.Draw("COLZ")
    pad2.cd(5)
    hitmapA4.Draw("COLZ")
    pad2.cd(6)
    hitmapA5.Draw("COLZ")

    # print DPTS hitmaps, correlations


    pad3.cd()
    pad3.Divide(len(regions_to_draw), 3)

    pad_index = 1

    for region in regions_to_draw:
            hitmap = getattr(fileRoot.EventLoaderEUDAQ2, region).Get("hitmap")
            hitmap.SetTitle(f"Hitmap {region}")
            pad3.cd(pad_index)
            hitmap.Draw("COLZ")
            pad_index += 1

    for region in regions_to_draw:
            correlationsX = getattr(fileRoot.Correlations, region).Get("correlationX_2Dlocal")
            correlationsX.SetTitle(f"Correlations X {region}")
            pad3.cd(pad_index)
            correlationsX.Draw("COLZ")
            pad_index += 1

    for region in regions_to_draw:
            correlationsY = getattr(fileRoot.Correlations, region).Get("correlationY_2Dlocal")
            correlationsY.SetTitle(f"Correlations Y {region}")
            pad3.cd(pad_index)
            correlationsY.Draw("COLZ")
            pad_index += 1
    
    c1.Update()
    filename = os.path.basename(corry_input).replace('.root', '.png')
    c1.Print(outputdir+"/"+os.path.basename(corry_input).replace('.root','.png'))