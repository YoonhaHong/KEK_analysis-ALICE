from common_imports import *

def main(argv):

    try:
        CHIPNAME = argv[1]
    except IndexError:
        print("Usage: script_name <CHIPNAME>")
        sys.exit(1)

    try:
        Halfunit = argv[2]
    except IndexError:
        print("Usage: script_name <Halfunit>")
        sys.exit(1)
    
    print(CHIPNAME)
    print(Halfunit)

    region_number = 3

    base_vcasb_collection = {

        # # ## for MOSS-5_W24B5, for ibias 62
        # # # tb (t7)
        # 0: list(range(79, 118, 3)),
        # 1: list(range(82, 121, 3)),
        # 2: list(range(88, 121, 3)), ## exclude 121, 124 too noisy
        # 3: list(range(79, 115, 3)), ## exclude 115 too noisy

        # ## for bb (b4)
        # 0: list(range(86, 125, 3)),
        # 1: list(range(86, 125, 3)),
        # 2: list(range(86, 125, 3)),
        # 3: list(range(70, 118, 3)),

        # ## for MOSS-5_W24B5, for ibias 124
        # # tb (t7)
        # 0: list(range(79, 115, 3)), ## exclude 115 too noisy
        # 1: list(range(82, 118, 3)), ## ver1, exclude 118 too noisy
        # 2: list(range(88, 124, 3)), ## exclude 124 too noisy
        # 3: list(range(79, 115, 3)), ## exclude 115 too noisy

        ## for bb (b4)
        0: list(range(86, 125, 3)),
        1: list(range(86, 122, 3)), 
        2: list(range(86, 113, 3)), ## 86 - 110
        3: list(range(70, 115, 3)), ## exclude 115 too noisy


        # ## for baby-5_2_W24B5, for ibias 62
        # # tb
        # 1: list(range(76, 115, 3)),
        # 2: list(range(85, 124, 3)), 
        # 3: list(range(77, 116, 3)),
        # # bb
        # 1: list(range(78, 117, 3)),
        # 2: list(range(78, 114, 3)), ## exclude 114 too noisy
        # 3: list(range(62, 110, 3)),

        # ## for baby-5_2_W24B5, for ibias 124
        # # tb
        # 0: list(range(79, 118, 3)),  
        # 1: list(range(76, 115, 3)),
        # 2: list(range(85, 124, 3)), 
        # 3: list(range(77, 116, 3)),
        # bb
        # 1: list(range(78, 117, 3)),
        # 2: list(range(78, 114, 3)), ## exclude 114 too noisy
        # 3: list(range(62, 110, 3)),

        # ## baby-4_4_W21D4
        # ## tb
        # 0: list(range(43, 82, 3)),
        # 1: list(range(43, 85, 3)),
        # 2: list(range(52, 94, 3)),
        # 3: list(range(45, 87, 3)),

        # # ## bb
        # 0: list(range(47, 89, 3)),
        # 3: list(range(36, 78, 3)),

        # ## W02F4
        # ## tb
        # 0: list(range(72, 114, 3)),
        # 1: list(range(69, 111, 3)),
        # 2: list(range(77, 119, 3)),
        # 3: list(range(70, 112, 3)),

        # # ## bb
        # 0: list(range(69, 111, 3)),
        # 1: list(range(69, 111, 3)),
        # 3: list(range(65, 107, 3)), 
         
    }

    if region_number not in base_vcasb_collection:
        print(f"Out of range: region number {region_number}")
        sys.exit(1)

    vcasb_List = base_vcasb_collection[region_number]
    print(vcasb_List)

    output_dir_local = "/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output"
    base_paths = {
        'babyMOSS-2_3_W04E2': {
            'tb': '%s/2024-08_PS_II/babyMOSS-2_3_W04E2/tb_psub12/region%d/VCASB%d',
            'bb': '%s/2024-08_PS_II/babyMOSS-2_3_W04E2/bb_psub12/region%d/VCASB%d',
        },
        'babyMOSS-2_3_W02F4': {
            'tb': '%s/2024-08_PS_II/babyMOSS-2_3_W02F4/tb_psub12/region%d/VCASB%d',
            'bb': '%s/2024-08_PS_II/babyMOSS-2_3_W02F4/bb_psub12/region%d/VCASB%d',
        },
        'babyMOSS-4_4_W21D4': {
            'tb': '%s/2024-09_PS/babyMOSS-4_4_W21D4/tb_psub12/region%d/VCASB%d',
            'bb': '%s/2024-09_PS/babyMOSS-4_4_W21D4/bb_psub12/region%d/VCASB%d',
        },
        'babyMOSS-5_2_W24B5_ibias62': { ## changed dir name manually VCASB_xx => VCASBxx
            'tb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/top/psub_12/ibias_62/region%d/VCASB%d',
            'bb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/bottom/psub_12/ibias_62/region%d/VCASB%d',
        },
        'babyMOSS-5_2_W24B5_ibias124': { 
            'tb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/top/psub_12/ibias_124/region%d/VCASB%d',
            'bb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/bottom/psub_12/ibias_124/region%d/VCASB%d',
        },
        'MOSS-5_W24B5_ibias62': { ## changed dir name manually VCASB_xx => VCASBxx
            'tb': '%s/2024-05_PS/MOSS-5_W24B5/t7/psub_12/ibias_62/region%d/VCASB%d',
            'bb': '%s/2024-05_PS/MOSS-5_W24B5/b4/psub_12/ibias_62/region%d/VCASB%d',
        },
        'MOSS-5_W24B5_ibias124': { 
            'tb': '%s/2024-05_PS/MOSS-5_W24B5/t7/psub_12/ibias_124/region%d/VCASB%d',
            'bb': '%s/2024-05_PS/MOSS-5_W24B5/b4/psub_12/ibias_124/region%d/VCASB%d',
        },
        'test': {},
    }

    if CHIPNAME not in base_paths:
        print(f"Unrecognised name {CHIPNAME}")
        sys.exit(1)

    # 모든 하위 딕셔너리에서 CHIPNAME가 존재하는지 확인
    Halfunit_found = any(Halfunit in paths for paths in base_paths.values())
    if not Halfunit_found:
        print(f"Unrecognised name {Halfunit}")
        sys.exit(1)

    list_eff = []
    list_eff_errlow = []
    list_eff_errup = []
    list_resX = []
    list_resX_err = []
    list_resY = []
    list_resY_err = []
    list_meanCl = []
    list_meanCl_err = []

    for index, vcasb in enumerate(vcasb_List):
        OPT_FNAME = f"{base_paths[CHIPNAME][Halfunit]}" % (output_dir_local, region_number, vcasb)
        print(OPT_FNAME)
        
        if not os.path.exists(OPT_FNAME):
            print(f"Error: The specified path does not exist: {OPT_FNAME}")
            sys.exit(1) 

        ## 3 is the 3rd plane in the telescope: 0, 1, 2 (ALPIDE) / DUT / 4, 5, 6 (ALPIDE)
        DUTname = "MOSS_reg%d_3"%(region_number)  

        input_file = ROOT.TFile("%s/%s_%s_analysis_reg%d.root" % (OPT_FNAME, CHIPNAME, Halfunit, region_number))

        residual_X_plot = input_file.Get(f"AnalysisDUT/{DUTname}/global_residuals/residualsX")
        residual_Y_plot = input_file.Get(f"AnalysisDUT/{DUTname}/global_residuals/residualsY")

        AssocClusterSize = input_file.Get(f"AnalysisDUT/{DUTname}/clusterSizeAssociated")

        EfficiencyPlot = input_file.Get(f"AnalysisEfficiency/{DUTname}/eTotalEfficiency")

        c0 = ROOT.TCanvas("c0","c0", 800, 1000)
        EfficiencyPlot.Draw()
        text0 = ROOT.TLatex(.65, .91, "Eff:%.6f"%(EfficiencyPlot.GetEfficiency(1)))
        text0.SetNDC(ROOT.kTRUE)
        text0.Draw()
        c0.Update()
        c0.SaveAs(f"{OPT_FNAME}/totalEfficiency_region_{region_number}_vcasb_{vcasb}.png")

        # print("====")
        # print(EfficiencyPlot.GetEfficiency(1))
        # print(input_file.Get(f"AnalysisEfficiency/{DUTname}/eTotalEfficiency").GetEfficiency(1))
        # print("====") 


        c1 = ROOT.TCanvas("c1","c1", 1600,1000)
        c1.Divide(2,1)
        c1.cd(1)
        residual_X_plot.Fit("gaus", "", "", -30, 30)
        residual_X_plot.SetAxisRange(-100, 100, "X")
        residual_X_plot.Draw()
        c1.cd(2)
        residual_Y_plot.Fit("gaus", "", "", -30, 30)
        residual_Y_plot.SetAxisRange(-100, 100, "X")
        residual_Y_plot.Draw()
        c1.Update()
        c1.SaveAs(f"{OPT_FNAME}/residual-X-and-Y_region_{region_number}_vcasb_{vcasb}.png")

        c2 = ROOT.TCanvas("c2","c2", 800, 1000)
        AssocClusterSize.Draw()
        c2.Update()
        c2.SaveAs(f"{OPT_FNAME}/AssocClusterSize_{region_number}_vcasb_{vcasb}.png")

        print(f"==== Done for region: {region_number} & vcasb: {vcasb} ====")

        list_eff.append(EfficiencyPlot.GetEfficiency(1))
        list_eff_errlow.append(EfficiencyPlot.GetEfficiencyErrorLow(1))
        list_eff_errup.append(EfficiencyPlot.GetEfficiencyErrorUp(1))

        list_resX.append(residual_X_plot.GetListOfFunctions().FindObject("gaus").GetParameter(2)) 
        list_resX_err.append(residual_X_plot.GetListOfFunctions().FindObject("gaus").GetParError(2))
        
        list_resY.append(residual_Y_plot.GetListOfFunctions().FindObject("gaus").GetParameter(2))
        list_resY_err.append(residual_Y_plot.GetListOfFunctions().FindObject("gaus").GetParError(2))

        list_meanCl.append(AssocClusterSize.GetMean())
        list_meanCl_err.append(AssocClusterSize.GetMeanError())

    if not len(vcasb_List) == len(list_eff) == len(list_resX) == len(list_resY) == len(list_meanCl):
        print("number of index does not matched!")
        sys.exit(1)

    array_vcasb = np.array(vcasb_List)
    array_eff = np.array(list_eff)
    array_eff_errlow = np.array(list_eff_errlow)
    array_eff_errup = np.array(list_eff_errup)
    array_resX = np.array(list_resX)
    array_resX_err = np.array(list_resX_err)
    array_resY = np.array(list_resY)
    array_resY_err = np.array(list_resY_err)
    array_meanCl = np.array(list_meanCl)
    array_meanCl_err = np.array(list_meanCl_err)
   
    pathname = "/".join(OPT_FNAME.split("/")[1:])
    pattern = r"/VCASB\d{2,3}"
    pathname_v2 = re.sub(pattern, '', pathname)
    print(pathname_v2)

    np.savez(f'/{pathname_v2}/{CHIPNAME}_{Halfunit}_reg{region_number}_data.npz', vcasb = array_vcasb,
              eff = array_eff, eff_errlow = array_eff_errlow, eff_errup = array_eff_errup,
              resX = array_resX, resX_err = array_resX_err, resY = array_resY, resY_err = array_resY_err,
              cluSize = array_meanCl, cluSize_err = array_meanCl_err, reg_num = region_number)


    csv_file = pd.DataFrame({
        'vcasb': vcasb_List,
        'eff': list_eff,
        'eff_errlow': list_eff_errlow,
        'eff_errup': list_eff_errup,
        'resX': list_resX,
        'resX_err': list_resX_err,
        'resY': list_resY,
        'resY_err': list_resY_err,
        'cluSize' : list_meanCl,
        'cluSize_err': list_meanCl_err,
        'reg_num': region_number
    })

    csv_file.to_csv(f'/{pathname_v2}/{CHIPNAME}_{Halfunit}_reg{region_number}_data.csv')
 


if __name__ == "__main__":
    main(sys.argv)





