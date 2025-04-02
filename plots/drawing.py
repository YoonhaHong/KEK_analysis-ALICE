import ROOT
import pandas as pd
import numpy as np
import re

def extract_values(root_file_path, dut_name, output_dir):
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
        print(f"failed to open: {root_file_path}")
        return None

    efficiency_path = f"AnalysisEfficiency/{dut_name}/eTotalEfficiency"
    efficiency_hist = root_file.Get(efficiency_path)
    eff = efficiency_hist.GetEfficiency(1)
    eff_errup = efficiency_hist.GetEfficiencyErrorUp(1)
    eff_errlow = efficiency_hist.GetEfficiencyErrorLow(1)

    clustersize_path = f"AnalysisDUT/{dut_name}/clusterSizeAssociated"
    clustersize_hist = root_file.Get(clustersize_path)
    cs = clustersize_hist.GetMean()
    cs_err = clustersize_hist.GetMeanError()

    residualX_path = f"AnalysisDUT/{dut_name}/local_residuals/residualsX"
    residualX_hist = root_file.Get(residualX_path)
    residualX_fit = residualX_hist.Fit("gaus", "Q", "", -30, 30)
    resX = residualX_hist.GetListOfFunctions().FindObject("gaus").GetParameter(2)
    resX_err = residualX_hist.GetListOfFunctions().FindObject("gaus").GetParError(2)

    residualY_path = f"AnalysisDUT/{dut_name}/local_residuals/residualsY"
    residualY_hist = root_file.Get(residualY_path)
    residualY_fit = residualY_hist.Fit("gaus", "Q", "", -30, 30)
    resY = residualY_hist.GetListOfFunctions().FindObject("gaus").GetParameter(2)
    resY_err = residualY_hist.GetListOfFunctions().FindObject("gaus").GetParError(2)
    
    #region_num = int(dut_name[-3])
    #if region_num == 0 or region_num == 3:
    #    trk_res = 4.66
    #elif region_num == 1 or region_num == 2:
    #    trk_res = 2.18
    #else:
    #    print("non sence region number in Get_Spatial_Resolution")
    #    return
    #trk_uncert = 0.41
    trk_res = 2.40

    spatial_resX = np.sqrt(resX**2 - trk_res**2)
    spatial_resY = np.sqrt(resY**2 - trk_res**2)
    spatial_res_mean = (spatial_resX + spatial_resY)/2
    # print(index, value, spatial_resX)
    # print(index, value, spatial_resY)
    
    #if region_num == 0 or region_num == 3:
    #    spatial_uncert_x = np.sqrt((resX/spatial_resX)**2 *(resX_err)**2 + (trk_res/spatial_resX)**2 *(trk_uncert)**2)
    #    spatial_uncert_y = np.sqrt((resY/spatial_resY)**2 *(resY_err)**2 + (trk_res/spatial_resY)**2 *(trk_uncert)**2)
    #elif region_num == 1 or region_num == 2:
    spatial_uncert_x = (resX/spatial_resX)*resX_err
    spatial_uncert_y = (resY/spatial_resY)*resY_err

    spatial_res_uncert = np.sqrt((spatial_uncert_x**2 + spatial_uncert_y**2)/4)
    
    return {"efficiency":eff, "efficiency_errorup":eff_errup, "efficiency_errorlow":eff_errlow,
            "residualsX": resX, "residualsX_error":resX_err,
            "residualsY": resY, "residualsY_error":resY_err,
            "spatialres":spatial_res_mean, "spatialres_error": spatial_res_uncert,
            "clustersize":cs, "clustersize_error":cs_err}

def Get_descriptions(dir_name):
    if "tb" in dir_name:
        hu = "Top"
        pitch = 22.5
    elif "bb" in dir_name:
        hu = "Bottom"
        pitch = 18.0

    ireset = 10 #default value
    if "IRESET" in dir_name:
        match = re.search(r"IRESET(\d{1,2})", dir_name)

        if match:
            ireset = match.group(1)

        lines = [
            "Non-Irradiated",
            "Wafer: W21D4",
            "Split: 2_4",
            f"Pitch: {pitch:.1f} \u03BCm",
            f"Half-unit: {hu}",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = "+f"{ireset} DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 24 \u00B0C",
        ]
        return lines
    
def Get_Spatial_Resolution(beam_data_list):

    print(beam_data_list.columns)
    print(beam_data_list['reg_num'][0])

    #region_num = beam_data_list['reg_num'][0]
    #if region_num == 0 or region_num == 3:
    #    trk_res = 4.66
    #elif region_num == 1 or region_num == 2:
    #    trk_res = 2.18
    #else:
    #    print("non sence region number in Get_Spatial_Resolution")
    #    sys.exit(1)
    #print("trk_res : ", trk_res)
    #trk_uncert = 0.41
    trk_res = 2.40

    vcasb_list =[]
    spatial_res_mean_list = []
    spatial_res_uncert_list = []


    for index, value in enumerate(beam_data_list['vcasb']):
        resX = beam_data_list['resX'][index]
        resY = beam_data_list['resY'][index]
        resX_err = beam_data_list['resX_err'][index]
        resY_err = beam_data_list['resY_err'][index]

        vcasb_list.append(value)
        spatial_resX = np.sqrt(resX**2 - trk_res**2)
        spatial_resY = np.sqrt(resY**2 - trk_res**2)
        spatial_res_mean = (spatial_resX + spatial_resY)/2
        spatial_res_mean_list.append(spatial_res_mean)

        # print(index, value, spatial_resX)
        # print(index, value, spatial_resY)

        #if region_num == 0 or region_num == 3:
        #    spatial_uncert_x = np.sqrt((resX/spatial_resX)**2 *(resX_err)**2 + (trk_res/spatial_resX)**2 *(trk_uncert)**2)
        #    spatial_uncert_y = np.sqrt((resY/spatial_resY)**2 *(resY_err)**2 + (trk_res/spatial_resY)**2 *(trk_uncert)**2)
        #elif region_num == 1 or region_num == 2:
        spatial_uncert_x = (resX/spatial_resX)*resX_err
        spatial_uncert_y = (resY/spatial_resY)*resY_err

        spatial_res_uncert = np.sqrt((spatial_uncert_x**2 + spatial_uncert_y**2)/4)
        spatial_res_uncert_list.append(spatial_res_uncert)
        print(value, spatial_res_mean, spatial_res_uncert)

    # print(len(beam_data_list['vcasb']))
    # print(vcasb_list)
    # print(spatial_res_mean_list)
    # print(spatial_res_uncert_list)


    combined = pd.DataFrame({
        'vcasb': vcasb_list,
        'spatial_res_mean': spatial_res_mean_list,
        'spatial_res_uncert': spatial_res_uncert_list
    })

    print(combined)

    return combined