import sys
import os
import ROOT
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import argparse
def extract_efficiency(root_file_path, dut_name, output_dir):
    """
    Extract efficiency and histograms from ROOT file.
    
    Args:
        root_file_path (str): Path to the ROOT file.
        dut_name (str): Name of the DUT (Detector Under Test).
        output_dir (str): Directory to save output files.
        
    Returns:
        tuple: (efficiency value, efficiency error) or (None, None) if not found.
    """
    root_file = ROOT.TFile.Open(root_file_path)
    if not root_file or root_file.IsZombie():
        print(f"ROOT 파일 열기 실패: {root_file_path}")
        return None

    efficiency_path = f"AnalysisEfficiency/{dut_name}/eTotalEfficiency"
    efficiency_hist = root_file.Get(efficiency_path)
    eff = efficiency_hist.GetEfficiency(1)
    eff_err = efficiency_hist.GetEfficiencyErrorUp(1)

    residualX_path = f"AnalysisDUT/{dut_name}/local_residuals/residualsX"
    residualX_hist = root_file.Get(residualX_path)
    residualX_fit = residualX_hist.Fit("gaus", "SQ")
    resX = residualX_fit.Parameter(1)
    resX_err = residualX_fit.Parameter(2)

    residualY_path = f"AnalysisDUT/{dut_name}/local_residuals/residualsY"
    residualY_hist = root_file.Get(residualY_path)
    residualY_fit = residualY_hist.Fit("gaus", "SQ")
    resY = residualY_fit.Parameter(1)
    resY_err = residualY_fit.Parameter(2)
    
    root_file.Close()
    
    return {"efficiency":eff, "efficiency_error":eff_err,
            "residualX":resX, "residualX_error":resX_err,
            "residualY":resY, "residualY_error":resY_err}


def analyze_efficiencies(base_dir, output_dir):
    """
    Analyze and collect efficiencies for all detectors.
    
    Args:
        base_dir (str): Base directory containing batch_analysis folders.
    
    Returns:
        pd.DataFrame: DataFrame containing efficiencies for each detector.
    """
    data = []
    
    for detector in os.listdir(base_dir):
        detector_path = os.path.join(base_dir, detector)
        if not os.path.isdir(detector_path):
            continue

        dut_name = detector[0:2] + "_reg" + detector[2] + "_3"
        
        for file in os.listdir(detector_path):
            if file.endswith(".root"):
                root_file_path = os.path.join(detector_path, file)
                match = re.search(r'VCASB(\d+)', file)
                VCASB = int(match.group(1)) if match else 1
                data.append({"Detector": detector} | {"VCASB": VCASB} | extract_efficiency(root_file_path, dut_name, output_dir) )
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Base directory containing batch_analysis folders
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str)
    parser.add_argument("--output_dir", type=str, required=False, default="./plots")
    args = parser.parse_args()
    base_directory = args.base_dir
    output_dir = os.path.join(args.output_dir, os.path.basename(base_directory))
    os.makedirs(output_dir, exist_ok=True)
    # Analyze efficiencies
    efficiency_df = analyze_efficiencies(base_directory, output_dir)
    # Save results to CSV
    efficiency_df.to_csv(f"{output_dir}/efficiency_results.csv", index=False)
    

    # Apply WP3 style settings
    plt.rcParams['figure.subplot.bottom'] = 0.13
    plt.rcParams['figure.subplot.top'] = 0.97
    plt.rcParams['figure.subplot.left'] = 0.13
    plt.rcParams['figure.subplot.right'] = 0.97
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['axes.prop_cycle'] = plt.cycler('color', ["#56B4E9", "#E69F00", "#009E73", "#CC79A7", "#0072B2", "#D55E00", "#F0E442"])
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['mathtext.default'] = 'regular'
    plt.rcParams['legend.fontsize'] = 14
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams['font.size'] = 14
    plt.rcParams['image.cmap'] = 'cividis'

    fig, ax1 = plt.subplots(figsize=(15.2, 7))
    plt.subplots_adjust(left=0.08, right=0.70, bottom=0.10, top=0.95)
    
    ax1.grid()
    ax1.set_xlabel(r'$\it{V_{casb}}$ [DAC]')
    ax1.set_ylabel('Detection Efficiency [%]')

    ax1.tick_params(axis='y')
    ax1.set_ylim(91,101)
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 11)) 

    ax1.axhline(y=99.0, color='grey', linestyle='--')
    print(ax1.get_xlim()[0])
    print(ax1.get_xlim()[1])
    print(ax1.get_xlim()[0]-0.014*(ax1.get_xlim()[1]-ax1.get_xlim()[0]))
    ax1.text(ax1.get_xlim()[0]-0.014*(ax1.get_xlim()[1]-ax1.get_xlim()[0]), 99, "99", fontsize=12, color='grey', ha='right', va='center')
    ax1.text(ax1.get_xlim()[0]*1.05, 99*1.00, "99", fontsize=12, color='grey', ha='right', va='center') ## ongoing 

    for detector in efficiency_df['Detector'].unique():
        detector_data = efficiency_df[efficiency_df['Detector'] == detector]
        detector_data = detector_data.sort_values('VCASB')  # VCASB 순서대로 정렬
        ax1.errorbar(detector_data['VCASB'], 
                detector_data['efficiency']*100., 
                yerr=detector_data['efficiency_error']*100., 
                fmt='o-', 
                label=detector)
        
    # 두 번째 y축 생성 (twinx를 사용해 ax1과 x축을 공유)
    ax2 = ax1.twinx()
    #ax2.errorbar([], [], ([], []), label="Detection efficiency", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Fake-hit rate", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')
    
    ax2.set_ylabel('Fake-hit rate [hits/pixel/event]')
    ax2.tick_params(axis='y')  
    ax2.set_ylim(0, 1e-1) #era -3
    ax2.set_yscale('symlog',linthresh=1e-10, linscale=0.90)
    ax2.set_yticks([0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])

    ax2.axhline(y=1e-6, color='grey', linestyle=':')
    ax2.text(ax2.get_xlim()[1]*0.99, 1e-6*1.70, "FHR measurement sensitivity limit", fontsize=9, color='grey', ha='right', va='top')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)
  


    
    plt.savefig(f"{output_dir}/efficiency_vs_VCASB.png")
    print(efficiency_df)