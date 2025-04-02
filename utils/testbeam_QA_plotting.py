#!/usr/bin/env python3

import os
import glob
import subprocess
#from rich import print
#from testbeam_QA_utils import *

import ROOT
#ROOT.gROOT.SetBatch(True)

def plot_QA_results(corry_input,outputdir,name):
    analyse_root = ROOT.TFile.Open(corry_input,"READ")
    regions = ["tb_reg0_3", "tb_reg1_3", "tb_reg2_3", "tb_reg3_3", "bb_reg0_3", "bb_reg1_3", "bb_reg2_3", "bb_reg3_3"]
    regions_to_draw = []
    for region in regions:
        if hasattr(analyse_root.EventLoaderEUDAQ2, region): regions_to_draw.append(region)
    print("Detected regions: ", regions_to_draw)
    nregion = len(regions_to_draw)

    _planes = [f"ALPIDE_{i}" for i in range(15)] 
    planes = []
    for plane in _planes:
        if hasattr(analyse_root.EventLoaderEUDAQ2, plane): planes.append(plane)
    print("Detected planes: ", planes)
    nplane = len(planes)

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
    alpide_index = 1
    for plane in planes:
        hitmap = getattr(analyse_root.EventLoaderEUDAQ2, plane).Get("hitmap")
        hitmap.SetTitle(f"Hitmap {plane}")
        pad2.cd(alpide_index)
        hitmap.Draw("COLZ")
        alpide_index+=1


    pad3.cd()
    pad3.Divide(len(regions_to_draw), 3)

    pad_index = 1

    for region in regions_to_draw:
            hitmap = getattr(analyse_root.EventLoaderEUDAQ2, region).Get("hitmap")
            hitmap.SetTitle(f"Hitmap {region}")
            pad3.cd(pad_index)
            hitmap.Draw("COLZ")
            pad_index += 1

    for region in regions_to_draw:
            correlationsX = getattr(analyse_root.Correlations, region).Get("correlationX_2Dlocal")
            correlationsX.SetTitle(f"Correlations X {region}")
            pad3.cd(pad_index)
            correlationsX.Draw("COLZ")
            pad_index += 1

    for region in regions_to_draw:
            correlationsY = getattr(analyse_root.Correlations, region).Get("correlationY_2Dlocal")
            correlationsY.SetTitle(f"Correlations Y {region}")
            pad3.cd(pad_index)
            correlationsY.Draw("COLZ")
            pad_index += 1
    
    c1.Update()
    filename = os.path.basename(corry_input).replace('.root', '.png')
    c1.Print(outputdir+"/"+os.path.basename(corry_input).replace('.root','.png'))
    
    input("Press any key to exit")

def draw_fit_result(fit_result, precision=0):
    """
    피팅 결과를 그리는 함수
    :param fit_result: 피팅 결과 객체
    :param precision: 소수점 자리수 (기본값: 0)
    """
    if fit_result.IsValid():
        mean_x = fit_result.Parameter(1)
        sigma_x = fit_result.Parameter(2)
        latex_x = ROOT.TLatex()
        latex_x.SetTextSize(0.08)
        latex_x.SetTextColor(2)  # 빨간색
        latex_x.DrawLatexNDC(0.15, 0.82, f"Mean: {mean_x:.{precision}f}")
        latex_x.DrawLatexNDC(0.15, 0.72, f"Sigma: {sigma_x:.{precision}f}")


def plot_QA_results_12ALPIDE(corry_input,outputdir,name):
    analyse_root = ROOT.TFile.Open(corry_input,"READ")
    _planes = [f"ALPIDE_{i}" for i in range(15)] 
    planes = []
    for plane in _planes:
        if hasattr(analyse_root.EventLoaderEUDAQ2, plane): planes.append(plane)
    print("Detected planes: ", planes)
    nplane = len(planes)


    c1 = ROOT.TCanvas('c1', 'c1', 0, 0, 2000, 2000)
    #                                        x1,  y1,  x2,  y2)
    pad1 = ROOT.TPad("pad1","This is pad1",0.01,0.92,0.99,0.99)
    pad2 = ROOT.TPad("pad3","This is pad3",0.01,0.22,0.99,0.92)
    pad3 = ROOT.TPad("pad2","This is pad2",0.01,0.01,0.99,0.22)
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

    pad_index = 1
    pad2.cd()
    pad2.Divide(12,5)
    for plane in range(12):
        for t in range(6):
           
            pad2.cd(pad_index + nplane * t)
            ROOT.gStyle.SetTextSize(0.1)
            if t == 0:
                clustermap = analyse_root.Get(f"ClusteringSpatial/ALPIDE_{plane}/clusterPositionLocal")     
                clustermap.Rebin2D(16, 16)
                clustermap.Draw("COLZ")
                print(" ")
            elif t == 1:
                hitmap = analyse_root.Get(f"EventLoaderEUDAQ2/ALPIDE_{plane}/hitmap")
                x_proj = hitmap.ProjectionX()
                x_proj.SetNameTitle(f"{plane}_xproj", f"{plane} projection X")
                fit_projX = x_proj.Fit("gaus", "SQ")  # 피팅 수행
                draw_fit_result(fit_projX)
            elif t == 2:
                hitmap = analyse_root.Get(f"EventLoaderEUDAQ2/ALPIDE_{plane}/hitmap")
                y_proj = hitmap.ProjectionY()
                y_proj.SetNameTitle(f"{plane}_yproj", f"{plane} projection Y")
                fit_projY = y_proj.Fit("gaus", "SQ")
                draw_fit_result(fit_projY)
                #y_proj.Draw()
            elif t ==3:
                corrX = analyse_root.Get(f"Correlations/ALPIDE_{plane}/correlationX")
                #corrX.SetNameTitle(f"{plane}_xcorr", f"{plane} correlation X")
                corrX.Draw()

            elif t ==4:
                corrY = analyse_root.Get(f"Correlations/ALPIDE_{plane}/correlationY")
                corrY.Draw()

            elif t == 5:
                pad_index += 1


    
    c1.Update()
    filename = os.path.basename(corry_input).replace('.root', '.png')
    c1.Print(outputdir+"/"+os.path.basename(corry_input).replace('.root','.png'))
    
    input("Press any key to exit")
