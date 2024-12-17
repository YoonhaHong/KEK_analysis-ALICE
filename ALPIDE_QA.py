import os
import sys
import shutil
import ROOT

def save_selected_hitmapograms_as_pdfs(root_file_path, output_dir):
    # ROOT 파일 열기
    root_file = ROOT.TFile.Open(root_file_path)
    if not root_file or root_file.IsZombie():
        print(f"Failed to open {root_file_path}")
        return

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 각 히스토그램 경로에 대해 반복
    regions = ["tb_reg1_3", "tb_reg2_3", "bb_reg1_3", "bb_reg2_3" ]
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)
    canvas.Divide(2, 2)
    canvas.SetLogz()
    cindex = 1
    for reg in regions:
        hitmap = root_file.Get(f"EventLoaderEUDAQ2/{reg}/hitmap")
        if not hitmap:
            print(f"{reg} hitmapogram  not found in the ROOT file.")
            continue

        canvas.cd( cindex )
        ROOT.gPad.SetLogz()
        hitmap.SetTitle( reg )
        hitmap.Rebin2D(8, 8)

        if "bb" in reg: 
 # Y축 데이터 반전
            hitmap.GetYaxis().SetTitle("320-Y")
            flipped_hitmap = hitmap.Clone(f"flipped_{hitmap.GetName()}")
            y_bins = hitmap.GetNbinsY()
            for x_bin in range(1, hitmap.GetNbinsX() + 1):
                    for y_bin in range(1, y_bins + 1):
                        flipped_hitmap.SetBinContent(x_bin, y_bins - y_bin + 1, hitmap.GetBinContent(x_bin, y_bin))
            flipped_hitmap.Draw("COLZ")
        else:
            hitmap.Draw("COLZ")
        cindex += 1

        

    output_pdf_path = os.path.join( output_dir, "MOSS_hitmap.pdf")
    canvas.SaveAs( output_pdf_path )
    print(f"Saved hitmapogram as {output_pdf_path}")

    # 파일 닫기
    root_file.Close()

if __name__ == "__main__":
    # 사용자 설정
    root_file_path = sys.argv[1]
    #output_dir = sys.argv[2]

    output_dir = root_file_path[:-5]
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    save_selected_hitmapograms_as_pdfs(root_file_path, output_dir )
