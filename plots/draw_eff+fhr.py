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
                data.append({"Detector": detector, "VCASB": VCASB} | extract_values(root_file_path, dut_name, output_dir))
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Argument parsing
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
    base_directory = args.base_dir.rstrip("/")  # Remove trailing "/"
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
        detector_data = efficiency_df[efficiency_df['Detector'] == detector].sort_values(xname)
        ax1.errorbar(detector_data[xname], 
                     detector_data['efficiency'] * 100., 
                     yerr=[detector_data['efficiency_errorlow'] * 100., detector_data['efficiency_errorup'] * 100.],
                     fmt='o', linestyle='-', 
                     label=f"{detector}")

    ax1.grid()
    if xscale == "THR":
        ax1.set_xlabel('Threshold [DAC]')
        ax1.set_xlim(10, 40)
    else:
        ax1.set_xlabel(r'$\it{V_{casb}}$ [DAC]')
    ax1.set_ylabel('Detection Efficiency [%]')

    ax1.tick_params(axis='y')
    ax1.set_ylim(91,101)
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 11)) 

    ax1.axhline(y=99.0, color='grey', linestyle='--')

    ax2 = ax1.twinx()
    ax2.errorbar([], [], ([], []), label="Detection efficiency", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Fake-hit rate", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')

    for detector in efficiency_df['Detector'].unique():
        detector_data = efficiency_df[efficiency_df['Detector'] == detector].sort_values(xname)
        ax2.errorbar(detector_data[xname], 
                     detector_data['MaskedFakeHitRate'],
                     yerr=[detector_data['MaskedFakeHitRateErrorLow'], detector_data['MaskedFakeHitRateErrorUp']],
                     fmt='o', linestyle='--', mfc='none', label=f"{detector}")

    ax2.set_ylabel('Fake-hit rate [hits/pixel/event]')
    ax2.tick_params(axis='y')  
    ax2.set_ylim(0, 1e-1) #era -3
    ax2.set_yscale('symlog',linthresh=1e-10, linscale=0.90)
    ax2.set_yticks([0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])

    ax2.axhline(y=1e-6, color='grey', linestyle=':')
    ax2.text(ax2.get_xlim()[1]*0.99, 1e-6*1.70, "FHR measurement sensitivity limit", fontsize=9, color='grey', ha='right', va='top')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)

    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)
    lines = Get_descriptions(dir_name=base_directory)
    multiline_text_legend = "\n".join(lines)
    #mask_line = Get_mask_info(Halfunit, CHIPNAME)
    lines_beam = [
        r'$\bf{ALICE}$ $\bf{ITS3}$ beam test $\it{WIP}$',
        '@ KEK PF-AR Mar 2025',
        r'5 GeV/$\it{c}$ electrons',
    ]
    multiline_text_beam = "\n".join(lines_beam)


    fig.text(1.13, 0.97, "babyMOSS-2_4_W21D4", fontweight='bold', transform=ax1.transAxes)
    fig.text(1.13, 0.94, multiline_text_legend.strip(), verticalalignment='top', horizontalalignment='left', transform=ax1.transAxes)
    fig.text(0.7, 0.955, multiline_text_beam.strip(), fontsize=13, ha='left', va='top',transform=ax1.transAxes)

    plt.savefig(f"{output_dir}/{os.path.basename(base_directory)}+effandfhr_vs_{xscale}.png")
    if platform.system() == "Darwin":  # macOS
       plt.show() 
