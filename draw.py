import os
import sys
import shutil
import ROOT

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

        if isinstance(hist, ROOT.TH1) or isinstance(hist, ROOT.TH2):
            # 히스토그램 이름에서 파일명 생성
            safe_hist_name = hist_path.replace("/", "_")
            output_pdf_path = os.path.join(output_dir, f"{safe_hist_name}.pdf")

            # 캔버스 생성 및 히스토그램 그리기
            canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
            hist.Draw("HIST")

            # PDF로 저장
            canvas.SaveAs(output_pdf_path)
            print(f"Saved histogram as {output_pdf_path}")
        else:
            print(f"'{hist_path}' is not a valid TH1 or TH2 histogram.")

    # 파일 닫기
    root_file.Close()

if __name__ == "__main__":
    # 사용자 설정
    root_file_path = sys.argv[1]
    #output_dir = sys.argv[2]

    # 저장하려는 히스토그램 경로 목록
    hist_paths = [
        "Tracking4D/trackChi2ndof",
        "Tracking4D/trackAngleX",
        "Tracking4D/trackAngleY",
        "Tracking4D/ALPIDE_7/local_residuals/LocalResidualsX"
    ]

    output_dir = root_file_path[:-5]
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    save_selected_histograms_as_pdfs(root_file_path, output_dir, hist_paths)
