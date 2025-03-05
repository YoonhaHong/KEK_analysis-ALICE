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
            #print(f"Histogram '{hist_path}' not found in the ROOT file.")
            continue

        safe_hist_name = hist_path.replace("/", "_")
        output_pdf_path = os.path.join(output_dir, f"{safe_hist_name}.pdf")
        hist.SetName( safe_hist_name )
        hist.SetTitle( safe_hist_name )
        
        if "hitmap" in hist_path:

            safe_hist_name = safe_hist_name[-15:-7]
            canvas = ROOT.TCanvas(safe_hist_name, "", 800, 400)
            hist.Rebin2D(16, 16)
            hist.Draw("COLZ")

            # x축 projection
            x_proj = hist.ProjectionX()
            x_proj.SetNameTitle(safe_hist_name + "_xproj", "")
            canvas_x = ROOT.TCanvas(safe_hist_name + "_xproj", "", 400, 400)
            x_proj.GetYaxis().SetRangeUser(0, x_proj.GetMaximum()*1.7)
            x_proj.Fit("gaus", "Q")
            x_proj.Draw()
            canvas_x.SaveAs(os.path.join(output_dir, f"{safe_hist_name}_xproj.pdf"))

            # y축 projection
            y_proj = hist.ProjectionY(safe_hist_name + "_yproj")
            y_proj.SetNameTitle(safe_hist_name + "_yproj", "")
            canvas_y = ROOT.TCanvas(safe_hist_name + "_yproj", "", 400, 400)
            y_proj.GetYaxis().SetRangeUser(0, y_proj.GetMaximum()*1.7)
            y_proj.Fit("gaus", "SQ")
            y_proj.Draw()
            canvas_y.SaveAs(os.path.join(output_dir, f"{safe_hist_name}_yproj.pdf"))

            
        elif "Chi2" in hist_path:
            canvas = ROOT.TCanvas(safe_hist_name, safe_hist_name, 800, 600)
            hist.GetXaxis().SetRangeUser(0, 10)
            hist.Draw()
        elif "residuals" in hist_path:
            canvas = ROOT.TCanvas(safe_hist_name, safe_hist_name, 800, 600)
            hist.GetXaxis().SetRangeUser(-60, 60)
            fit = hist.Fit("gaus", "SQ")
            hist.Draw()
            
            

        #elif "residuals" in hist_path:
        #    canvas = ROOT.TCanvas(safe_hist_name, safe_hist_name, 800, 600)
        #    ROOT.gPad.DrawFrame(-60, 0, 60, 500)
        #    hist.Draw("SAME HIST")
            

        
        else:
            canvas = ROOT.TCanvas(safe_hist_name, safe_hist_name, 800, 600)
            hist.Draw()


        canvas.SaveAs(output_pdf_path)
        #print(f"Saved histogram as {output_pdf_path}")

    # 파일 닫기
    root_file.Close()

if __name__ == "__main__":
    # 사용자 설정
    root_file_path = sys.argv[1]
    #output_dir = sys.argv[2]
    ROOT.gStyle.SetOptFit(111)  # Fit statistics box
    #ROOT.gStyle.SetStatStyle(0)
        

    # 저장하려는 히스토그램 경로 목록
    hist_paths = [
        "Tracking4D/trackChi2ndof",
        "Tracking4D/trackAngleX",
        "Tracking4D/trackAngleY",
        ""
    ]


    for i in [0,1,2,5,6,7]: 
        #hist_paths.append( f"Tracking4D/ALPIDE_{i}/hitmap")
        hist_paths.append( f"Tracking4D/ALPIDE_{i}/local_residuals/LocalResidualsX")
        hist_paths.append( f"Tracking4D/ALPIDE_{i}/local_residuals/LocalResidualsY")
        hist_paths.append( f"EventLoaderEUDAQ2/ALPIDE_{i}/hitmap")
    
    DUTs = ["tb_reg1_3", "tb_reg2_3",
            "bb_reg1_3", "bb_reg2_3",]
    for dut in DUTs:
        hist_paths.append( f"AnalysisDUT/{dut}/local_residuals/residualsX")
        hist_paths.append( f"AnalysisDUT/{dut}/local_residuals/residualsY")
        hist_paths.append( f"AnalysisEfficiency/{dut}/eTotalEfficiency")
        hist_paths.append( f"AnalysisEfficiency/{dut}/distanceTrackHit2D")
    

    output_dir = root_file_path[:-5]
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    save_selected_histograms_as_pdfs(root_file_path, output_dir, hist_paths)
