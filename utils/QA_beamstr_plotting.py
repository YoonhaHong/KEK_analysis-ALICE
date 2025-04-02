#!/usr/bin/env python3

import os
import glob
import subprocess
from rich import print
#from testbeam_QA_utils import *

import ROOT
from ROOT import TLatex
#ROOT.gROOT.SetBatch(True)



def draw_fit_result(fit_result, precision=0):
    """
    피팅 결과를 그리는 함수
    :param fit_result: 피팅 결과 객체
    :param precision: 소수점 자리수 (기본값: 0)
    """
    if fit_result.IsValid():
        mean_x = fit_result.Parameter(1)
        sigma_x = fit_result.Parameter(2)
        latex_x = TLatex()
        latex_x.SetTextSize(0.08)
        latex_x.SetTextColor(2)  # 빨간색
        latex_x.DrawLatexNDC(0.15, 0.82, f"Mean: {mean_x:.{precision}f}")
        latex_x.DrawLatexNDC(0.15, 0.72, f"Sigma: {sigma_x:.{precision}f}")

def plot_beamstr(rootfile,outputdir):

    analyse_root = ROOT.TFile.Open(rootfile,"READ")
    _planes = [f"ALPIDE_{i}" for i in range(15)] 
    planes = []
    for plane in _planes:
        if hasattr(analyse_root.EventLoaderEUDAQ2, plane): planes.append(plane)
    print("Detected planes: ", planes)
    nplane = len(planes)

    c1 = ROOT.TCanvas('c1', 'c1', 0, 0, 300*nplane, 1000)
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
    title.DrawLatex(.05,0.1,str(rootfile))
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

    pad_index = 1
    pad2.cd()
    pad2.Divide(nplane, 5)

    for plane in planes:
        for t in range(6):
           
            pad2.cd(pad_index + nplane * t)
            ROOT.gStyle.SetTextSize(0.1)
            if t == 0:
                #pad2.cd(pad_index)
                clustermap = analyse_root.Get(f"ClusteringSpatial/{plane}/clusterPositionLocal")
                #clustermap.Rebin2D(16, 16)
                clustermap.Draw("COLZ")
            elif t == 1:
                hitmap = getattr(analyse_root.EventLoaderEUDAQ2, plane).Get("hitmap")
                x_proj = hitmap.ProjectionX()
                x_proj.SetNameTitle(f"{plane}_xproj", f"{plane} projection X")
                fit_projX = x_proj.Fit("gaus", "SQ")  # 피팅 수행
                draw_fit_result(fit_projX)
            elif t == 2:
                hitmap = getattr(analyse_root.EventLoaderEUDAQ2, plane).Get("hitmap")
                y_proj = hitmap.ProjectionY()
                y_proj.SetNameTitle(f"{plane}_yproj", f"{plane} projection Y")
                fit_projY = y_proj.Fit("gaus", "SQ")
                draw_fit_result(fit_projY)
                #y_proj.Draw()
            elif t ==3:
                corrX = analyse_root.Get(f"Correlations/{plane}/correlationX")
                #corrX.SetNameTitle(f"{plane}_xcorr", f"{plane} correlation X")
                corrX.Draw()

            elif t ==4:
                corrY = analyse_root.Get(f"Correlations/{plane}/correlationY")
                corrY.Draw()

            elif t == 5:
                pad_index += 1
          
    pad3.cd()
    pad3.Divide(3,1)

    pad3.cd(1)
    trackX = analyse_root.Get(f"Tracking4D/trackAngleX")
    fit_trackX = trackX.Fit("gaus", "SQ")
    draw_fit_result(fit_trackX, precision=4)
    #trackX.Draw()

    pad3.cd(2)
    trackY = analyse_root.Get(f"Tracking4D/trackAngleY")
    fit_trackY = trackY.Fit("gaus", "SQ")
    draw_fit_result(fit_trackY, precision=4)

    #trackY.Draw()

    pad3.cd(3)
    trackchi2ndof = analyse_root.Get(f"Tracking4D/trackChi2ndof")
    trackchi2ndof.Draw()
    
    #c1.Update()
    c1.Print(outputdir+"/"+os.path.basename(rootfile).replace('.root','.png'))
    #ROOT.gPad.Update()
    #c1.Update()
    input("Press any key to exit")
    
