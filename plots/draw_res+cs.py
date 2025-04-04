'''
Drawing Spatial-Resolution & Cluster-Size as a function of VCASB
by Yoonha Hong
'''
import sys
import os
import platform
import ROOT
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import argparse
from datetime import date, datetime
from drawing import *



def extract_value_from_dir(base_dir, output_dir):
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
                data.append({"Detector": detector, "VCASB": VCASB} | extract_values(root_file_path, dut_name, output_dir) )
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Base directory containing batch_analysis folders
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str)
    parser.add_argument("-o", "--output_dir", type=str, required=False, default=".")
    parser.add_argument("-t", "--thr_csv", type=str, default="./THR_summary.csv", help="Path to THR_summary.csv")
    parser.add_argument("-f", "--fhr_csv", type=str, default="./FHR_summary.csv", help="Path to FHR_summary.csv")
    
    xscale = input("Plot as a function of THR or VCASB? (Type THR/VCASB)    ")
    if not xscale in ["THR", "VCASB"]: quit()
    elif xscale == "THR":
        xname = "ThresholdAverage"
    elif xscale == "VCASB":
        xname = xscale


    args = parser.parse_args()
    base_directory = args.base_dir[:-1] if args.base_dir.endswith("/") else args.base_dir # delete "/"
    output_dir = os.path.join(args.output_dir, os.path.basename(base_directory))
    os.makedirs(output_dir, exist_ok=True)

    csv_path = f"{output_dir}/{os.path.basename(base_directory)}+efficiency_results.csv" 
    if os.path.exists(csv_path): 
        print(f"Skipping extracting values, {csv_path} detected!")
        efficiency_df = pd.read_csv(csv_path)
    else:   
        efficiency_df = extract_value_from_dir(base_directory, output_dir)
        efficiency_df.to_csv(csv_path, index=False)
    efficiency_df = efficiency_df.sort_values('Detector')
    
    thr_df = pd.read_csv(args.thr_csv)
    # Add THR values
    efficiency_df = efficiency_df.merge(
    thr_df[['Detector', 'VCASB', 'ThresholdAverage', 'ThresholdRMS']],
        on=['Detector', 'VCASB'],
        how='left')
    
    fhr_df = pd.read_csv(args.fhr_csv)
    # Add FHR values
    efficiency_df = efficiency_df.merge(
    fhr_df[['Detector', 'VCASB', 'MaskedFakeHitRate','MaskedFakeHitRateErrorUp','MaskedFakeHitRateErrorLow']],
        on=['Detector', 'VCASB'],
        how='left')

    print(efficiency_df.head(5))
    

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

    for detector in efficiency_df['Detector'].unique():
        detector_data = efficiency_df[efficiency_df['Detector'] == detector]
        detector_data = detector_data.sort_values('VCASB')  # VCASB 순서대로 정렬
        ax1.errorbar(detector_data[xname], 
                detector_data['spatialres'], 
                yerr=detector_data['spatialres_error'],
                fmt='o', linestyle='-',
                label=f"{detector}")
    ax1.grid()
    if xscale == "THR":
        ax1.set_xlabel('Threshold [DAC]')
        ax1.set_xlim(10, 40)
    else:
        ax1.set_xlabel(r'$\it{V_{casb}}$ [DAC]')

    ax1.set_ylabel('Spatial resolution [\u03BCm]')
    ax1.tick_params(axis='y')


    if "tb" in base_directory:
        pitch = 22.5 / np.sqrt(12)
    elif "bb" in base_directory:
        pitch = 18.0 / np.sqrt(12)
    ax1.axhline(y=pitch, color='grey', linestyle=':')
    ax1.text(ax1.get_xlim()[0]*1.05, pitch, r"Pixel Pitch/$\sqrt{12}", fontsize=12, color='grey', ha='right', va='center') ## ongoing 

    # 두 번째 y축 생성 (twinx를 사용해 ax1과 x축을 공유)
    ax2 = ax1.twinx()
    ax2.errorbar([], [], ([], []), label="Spatial resolution", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Cluster size", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')
    for detector in efficiency_df['Detector'].unique():
        detector_data = efficiency_df[efficiency_df['Detector'] == detector]
        detector_data = detector_data.sort_values('VCASB')  # VCASB 순서대로 정렬
        ax2.errorbar(detector_data[xname], 
                detector_data['clustersize'], 
                yerr=detector_data['clustersize_error'],
                fmt='o',  linestyle='--', mfc='none',
                label=f"{detector}")
    ax2.set_ylabel('Average cluster size [pixels]')
    ax2.tick_params(axis='y') 
    # ax2.set_ylim(91,101) 
    # ax1.set_ylim(91,101)
    # ax1.set_xlim(45,130)
    # ax1.axhline(y=99.0, color='grey', linestyle='--')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)

    lines = Get_descriptions(dir_name=base_directory)
    multiline_text_legend = "\n".join(lines)
    #mask_line = Get_mask_info(Halfunit, CHIPNAME)
    plot_date = str(date.today().day) + ' ' + datetime.now().strftime("%b") + ' ' + str(date.today().year)
    lines_beam = [
        r'$\bf{ALICE}$ $\bf{ITS3}$ beam test $\it{WIP}$',
        '@ KEK PF-AR Mar 2025',
        r'5 GeV/$\it{c}$ electrons',
        'Plotted on {}'.format(plot_date),
    ]
    multiline_text_beam = "\n".join(lines_beam)

    fig.text(1.13, 0.97, "babyMOSS-2_4_W21D4", fontweight='bold', transform=ax1.transAxes)
    fig.text(1.13, 0.94, multiline_text_legend.strip(), verticalalignment='top', horizontalalignment='left', transform=ax1.transAxes)
    fig.text(0.01, 0.955, multiline_text_beam.strip(), fontsize=13, ha='left', va='top',transform=ax1.transAxes)
    #fig.text(0.01, 0.025, f'{mask_line}', fontsize=9, color='black', ha='left', va='center', transform=ax1.transAxes)
    plt.savefig(f"{output_dir}/{os.path.basename(base_directory)}+resolandclust_vs_{xscale}.png")
    if platform.system() == "Darwin":  # macOS
       plt.show() 
