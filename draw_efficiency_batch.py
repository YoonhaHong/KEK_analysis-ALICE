import sys
import os
import ROOT
import pandas as pd
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
    try:
        root_file = ROOT.TFile.Open(root_file_path)
        if not root_file or root_file.IsZombie():
            print(f"ROOT 파일 열기 실패: {root_file_path}")
            return None, None
        
        # 히스토그램 저장을 위한 캔버스 생성
        canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
        
        # hCutHisto 추출 및 저장
        histo_path = f"AnalysisDUT/{dut_name}/hCutHisto"
        histo = root_file.Get(histo_path)
        if histo:
            # 파일명에서 THR 값 추출
            match = re.search(r'THR(\d+)', root_file_path)
            thr_value = match.group(1) if match else "unknown"
            
            # PDF 파일명 생성
            pdf_name = f"{output_dir}/hCutHisto_{dut_name}_THR{thr_value}.pdf"
            
            # 히스토그램 그리기 및 저장
            histo.Draw("HIST TEXT")
            canvas.SaveAs(pdf_name)
        
        # 효율 추출 (기존 코드)
        efficiency_path = f"AnalysisEfficiency/{dut_name}/eTotalEfficiency"
        efficiency_hist = root_file.Get(efficiency_path)
        
        if efficiency_hist:
            eff = efficiency_hist.GetEfficiency(1)
            err = efficiency_hist.GetEfficiencyErrorUp(1)
            return eff, err
        else:
            print(f"효율 경로를 찾을 수 없음: {efficiency_path}")
            return None, None
    finally:
        if root_file:
            root_file.Close()

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
            if not file.startswith("prealign") and file.endswith(".root"):
                root_file_path = os.path.join(detector_path, file)
                match = re.search(r'THR(\d+)', file)
                threshold = int(match.group(1)) if match else None

                efficiency, error = extract_efficiency(root_file_path, dut_name, output_dir)
                data.append({
                    "Detector": detector,
                    "Threshold": threshold,
                    "Efficiency": efficiency,
                    "Error": error
                })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Base directory containing batch_analysis folders
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str)
    parser.add_argument("--output_dir", type=str, required=False, default="./figures")
    args = parser.parse_args()
    base_directory = args.base_dir
    output_dir = os.path.join(args.output_dir, os.path.basename(base_directory))
    os.makedirs(output_dir, exist_ok=True)
    # Analyze efficiencies
    efficiency_df = analyze_efficiencies(base_directory, output_dir)
    
    # Save results to CSV
    efficiency_df.to_csv(f"{output_dir}/efficiency_results.csv", index=False)
    
    # 각 detector별로 그래프 그리기
    plt.figure(figsize=(10, 6))
    
    for detector in efficiency_df['Detector'].unique():
        detector_data = efficiency_df[efficiency_df['Detector'] == detector]
        detector_data = detector_data.sort_values('Threshold')  # Threshold 순서대로 정렬
        plt.errorbar(detector_data['Threshold'], 
                detector_data['Efficiency'], 
                yerr=detector_data['Error'], 
                fmt='o-', 
                label=detector)
    
    plt.xlabel('Threshold [DAC]')
    plt.ylabel('Efficiency')
    plt.xlim(10, 35)
    plt.ylim(0.84, 1.00)
    plt.title('Detector Efficiency vs Threshold')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{output_dir}/efficiency_vs_threshold.png")
    print(efficiency_df)