import os
import sys
import shutil
import ROOT

xrange = [-10, -2, 2, 10]

def extract_x_minus_y(th2, x_min, x_max, output_name):
    """
    주어진 TH2F에서 특정 x축 범위 내에서 x - y를 계산하여 TH1F로 저장
    
    Parameters:
        th2 (ROOT.TH2F): 입력 TH2F 히스토그램
        x_min (float): x축 최소값
        x_max (float): x축 최대값
        output_name (str): 출력 TH1F 이름
    Returns:
        ROOT.TH1F: 생성된 TH1F 히스토그램
    """
    # 입력 히스토그램 정보 확인
    x_bins = th2.GetNbinsX()
    y_bins = th2.GetNbinsY()

    # x축의 bin 찾기
    x_min_bin = th2.GetXaxis().FindBin(x_min)
    x_max_bin = th2.GetXaxis().FindBin(x_max)

    # 출력 TH1F 생성
    th1 = ROOT.TH1F(output_name, f"{output_name};x_{{ref}}-x;Counts", 1000, -10.01, 9.99)  

    # x_min_bin ~ x_max_bin 범위의 데이터 순회
    for x_bin in range(x_min_bin, x_max_bin + 1):
        for y_bin in range(1, y_bins + 1):
            x = th2.GetXaxis().GetBinCenter(x_bin)
            y = th2.GetYaxis().GetBinCenter(y_bin)
            value = th2.GetBinContent(x_bin, y_bin)

            th1.Fill(y-x, value)

    return th1

def save_selected_histograms_as_pdfs(root_file_path, output_dir, hist_paths):
    # ROOT 파일 열기
    root_file = ROOT.TFile.Open(root_file_path)
    if not root_file or root_file.IsZombie():
        print(f"Failed to open {root_file_path}")
        return

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 각 히스토그램 경로에 대해 반복
    for hist_path in hist_paths:
        hist = root_file.Get(hist_path)

        if not hist:
            print(f"Histogram '{hist_path}' not found in the ROOT file.")
            continue



        elif isinstance(hist, ROOT.TH1) or isinstance(hist, ROOT.TH2):
            safe_hist_name = hist_path.replace("/", "_")
            output_pdf_path = os.path.join(output_dir, f"{safe_hist_name}.pdf")

            canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
            if("correlationX_2D" in hist_path):
                for i in range( len(xrange)-1 ):
                    XMIN = xrange[i]
                    XMAX = xrange[i+1]
                    c1 = ROOT.TCanvas("cutted", "cutted", 800, 600)
                    c1.cd()
                    corr1d = extract_x_minus_y(hist, XMIN, XMAX, "correlationX_1D")
                    corr1d.Draw("HIST")
                    latex1 = ROOT.TLatex()
                    latex1.SetNDC()  # NDC 좌표계 사용
                    latex1.DrawLatex(0.2, 0.85, f"{XMIN} < x < {XMAX}")  # 텍스트 1
                    output_path = os.path.join(output_dir, f"{safe_hist_name}_cutted_{XMIN}_{XMAX}.pdf")
                    c1.SaveAs(output_path)
                
            canvas.cd()
            hist.Draw()
            canvas.SaveAs(output_pdf_path)
            print(f"Saved histogram as {output_pdf_path}")
        
        else:
            print(f"'{hist_path}' is not a valid TH1 or TH2 histogram.")

    # 파일 닫기
    root_file.Close()



if __name__ == "__main__":
    ROOT.gStyle.SetTextFont(42)  # Helvetica, 일반 글꼴
    ROOT.gStyle.SetTextSize(0.06)
    ROOT.gStyle.SetOptStat(1110)  # 표시할 통계 정보 설정 (entries, mean, RMS 등)
    ROOT.gStyle.SetStatStyle(0)   # StatBox 배경 스타일 (0: 투명)
    ROOT.gStyle.SetStatBorderSize(1)  # 테두리 크기 조정 (0으로 하면 테두리 제거)
    # 사용자 설정
    root_file_path = sys.argv[1]
    #output_dir = sys.argv[2]

    # 저장하려는 히스토그램 경로 목록
    hist_paths = [] #Prealignment/ALPIDE_NUM/correlationX
    for i in [1,2,4,5,6,7]: 
        hist_paths.append( f"Prealignment/ALPIDE_{i}/correlationX")
        hist_paths.append( f"Prealignment/ALPIDE_{i}/correlationY")
        hist_paths.append( f"Prealignment/ALPIDE_{i}/correlationX_2D")

    output_dir = root_file_path[:-5]
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    save_selected_histograms_as_pdfs(root_file_path, output_dir, hist_paths)
