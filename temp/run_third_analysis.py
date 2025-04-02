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

    output_dir_local = "/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output"
    base_paths = {
        'babyMOSS-2_3_W04E2': {
            'tb': '%s/2024-08_PS_II/babyMOSS-2_3_W04E2/tb_psub12/region%d',
            'bb': '%s/2024-08_PS_II/babyMOSS-2_3_W04E2/bb_psub12/region%d',
        },
        'babyMOSS-2_3_W02F4': {
            'tb': '%s/2024-08_PS_II/babyMOSS-2_3_W02F4/tb_psub12/region%d',
            'bb': '%s/2024-08_PS_II/babyMOSS-2_3_W02F4/bb_psub12/region%d',
        },

        'babyMOSS-4_4_W21D4': {
            'tb': '%s/2024-09_PS/babyMOSS-4_4_W21D4/tb_psub12/region%d',
            'bb': '%s/2024-09_PS/babyMOSS-4_4_W21D4/bb_psub12/region%d',
        },
        'babyMOSS-5_2_W24B5_ibias62': { ## changed dir name manually VCASB_xx => VCASBxx
            'tb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/top/psub_12/ibias_62/region%d',
            'bb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/bottom/psub_12/ibias_62/region%d',
        },
        'babyMOSS-5_2_W24B5_ibias124': {
            'tb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/top/psub_12/ibias_124/region%d',
            'bb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/bottom/psub_12/ibias_124/region%d',
        },
        'MOSS-5_W24B5_ibias62': { ## changed dir name manually VCASB_xx => VCASBxx
            'tb': '%s/2024-05_PS/MOSS-5_W24B5/t7/psub_12/ibias_62/region%d',
            'bb': '%s/2024-05_PS/MOSS-5_W24B5/b4/psub_12/ibias_62/region%d',
        },
        'MOSS-5_W24B5_ibias124': { 
            'tb': '%s/2024-05_PS/MOSS-5_W24B5/t7/psub_12/ibias_124/region%d',
            'bb': '%s/2024-05_PS/MOSS-5_W24B5/b4/psub_12/ibias_124/region%d',
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

    ## make a empty list having a length of 4
    beam_data_list = [None] * 4
    fhr_data_list = [None] * 4
    thr_data_list = [None] * 4
    spa_data_list = [None] * 4  

    Switches = [True, True, True, True]
    Switches_list = [i for i, switch in enumerate(Switches) if switch]
    print(Switches_list) 

    if (Switches[0]): beam_data_list.insert(0, pd.read_csv(f'{base_paths[CHIPNAME][Halfunit]}/{CHIPNAME}_{Halfunit}_reg0_data.csv'%(output_dir_local, 0)))
    if (Switches[1]): beam_data_list.insert(1, pd.read_csv(f'{base_paths[CHIPNAME][Halfunit]}/{CHIPNAME}_{Halfunit}_reg1_data.csv'%(output_dir_local, 1)))
    if (Switches[2]): beam_data_list.insert(2, pd.read_csv(f'{base_paths[CHIPNAME][Halfunit]}/{CHIPNAME}_{Halfunit}_reg2_data.csv'%(output_dir_local, 2)))
    if (Switches[3]): beam_data_list.insert(3, pd.read_csv(f'{base_paths[CHIPNAME][Halfunit]}/{CHIPNAME}_{Halfunit}_reg3_data.csv'%(output_dir_local, 3)))

    Load_FHR_THR_files(fhr_data_list, thr_data_list, Halfunit, CHIPNAME)
    ### print(filename_something.column) ## to figure out the list of object/list names

    if (Switches[0]): spa_data_list[0] = Get_Spatial_Resolution(beam_data_list[0])
    if (Switches[1]): spa_data_list[1] = Get_Spatial_Resolution(beam_data_list[1])
    if (Switches[2]): spa_data_list[2] = Get_Spatial_Resolution(beam_data_list[2])
    if (Switches[3]): spa_data_list[3] = Get_Spatial_Resolution(beam_data_list[3])

    # print(spa_data_list[0]['vcasb'])
    # print(spa_data_list[0]['spatial_res_mean'])
    # print(spa_data_list[0]['spatial_res_uncert'])
    # print(beam_data_list[0].column)
    # print(beam_data_list[0]['cluSize'])
    # print(beam_data_list[0]['cluSize_err'])

    num = 2
    # ## TO exclude last points if there is additional points in THR/FHR
    print(beam_data_list[num]['vcasb'][::-1])
    print( thr_data_list[num]['vcasb'][::-1])
    print( fhr_data_list[num]['vcasb'][::-1])

    # # # 맨 뒤 요소 제외 
    ### (baby4-4_w21D4, tb, reg0, thr+fhr / baby5-2_w24B5_ibias62, bb, reg2, all / baby5-2_w24B5_ibias124, bb, reg2, thr+fhr)
    # beam_data_list[2] = beam_data_list[2].iloc[:-1].reset_index(drop=True)
    # spa_data_list[2] = spa_data_list[2].iloc[:-1].reset_index(drop=True)
   
    # ### MOSS-5_W24B5_62,tb,reg2-thr-fhr-2,reg3-thr-fhr-1
    # thr_data_list[2] = thr_data_list[2].iloc[:-2].reset_index(drop=True)
    # fhr_data_list[2] = fhr_data_list[2].iloc[:-2].reset_index(drop=True)
    # thr_data_list[3] = thr_data_list[3].iloc[:-1].reset_index(drop=True)
    # fhr_data_list[3] = fhr_data_list[3].iloc[:-1].reset_index(drop=True)
    # ## MOSS-5_W24B5_124,tb, all-regs
    # thr_data_list[0] = thr_data_list[0].iloc[:-1].reset_index(drop=True)
    # fhr_data_list[0] = fhr_data_list[0].iloc[:-1].reset_index(drop=True)
    # thr_data_list[1] = thr_data_list[1].iloc[:-1].reset_index(drop=True)
    # fhr_data_list[1] = fhr_data_list[1].iloc[:-1].reset_index(drop=True)
    # thr_data_list[2] = thr_data_list[2].iloc[:-1].reset_index(drop=True)
    # fhr_data_list[2] = fhr_data_list[2].iloc[:-1].reset_index(drop=True)
    # thr_data_list[3] = thr_data_list[3].iloc[:-1].reset_index(drop=True)
    # fhr_data_list[3] = fhr_data_list[3].iloc[:-1].reset_index(drop=True)
    ## MOSS-5_W24B5_124,bb, reg1,2,3
    thr_data_list[1] = thr_data_list[1].iloc[:-1].reset_index(drop=True)
    fhr_data_list[1] = fhr_data_list[1].iloc[:-1].reset_index(drop=True)
    thr_data_list[2] = thr_data_list[2].iloc[:-4].reset_index(drop=True)
    fhr_data_list[2] = fhr_data_list[2].iloc[:-4].reset_index(drop=True)
    thr_data_list[3] = thr_data_list[3].iloc[:-1].reset_index(drop=True)
    fhr_data_list[3] = fhr_data_list[3].iloc[:-1].reset_index(drop=True)
   
    print(beam_data_list[num]['vcasb'][::-1])
    print( thr_data_list[num]['vcasb'][::-1])
    print( fhr_data_list[num]['vcasb'][::-1])


    print(len(beam_data_list[num]['vcasb']))
    print( len(thr_data_list[num]['vcasb']))
    print( len(fhr_data_list[num]['vcasb']))
    print("=============================")


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

    # Figure와 첫 번째 Axes 생성
    fig, ax1 = plt.subplots(figsize=(15.2, 7))
    plt.subplots_adjust(left=0.08, right=0.70, bottom=0.10, top=0.95)

    # 첫 번째 y축에 대한 데이터 플롯
    if (Switches[0]): ax1.errorbar(beam_data_list[0]['vcasb'], beam_data_list[0]['eff']*100, 
                 yerr=[(beam_data_list[0]['eff_errlow']/beam_data_list[0]['eff'])*beam_data_list[0]['eff']*100, 
                       (beam_data_list[0]['eff_errup']/beam_data_list[0]['eff'])*beam_data_list[0]['eff']*100], 
                       fmt='o', linestyle='-', label='Region 0', color='#56B4E9') ## blue
    if (Switches[1]): ax1.errorbar(beam_data_list[1]['vcasb'], beam_data_list[1]['eff']*100, 
                 yerr=[(beam_data_list[1]['eff_errlow']/beam_data_list[1]['eff'])*beam_data_list[1]['eff']*100, 
                       (beam_data_list[1]['eff_errup']/beam_data_list[1]['eff'])*beam_data_list[1]['eff']*100], 
                       fmt='o', linestyle='-', label='Region 1', color='#E69F00') ## bright orange
    if (Switches[2]): ax1.errorbar(beam_data_list[2]['vcasb'], beam_data_list[2]['eff']*100, 
                 yerr=[(beam_data_list[2]['eff_errlow']/beam_data_list[2]['eff'])*beam_data_list[2]['eff']*100, 
                       (beam_data_list[2]['eff_errup']/beam_data_list[2]['eff'])*beam_data_list[2]['eff']*100], 
                       fmt='o', linestyle='-', label='Region 2', color='#009E73') ## green
    if (Switches[3]): ax1.errorbar(beam_data_list[3]['vcasb'], beam_data_list[3]['eff']*100, 
                 yerr=[(beam_data_list[3]['eff_errlow']/beam_data_list[3]['eff'])*beam_data_list[3]['eff']*100, 
                       (beam_data_list[3]['eff_errup']/beam_data_list[3]['eff'])*beam_data_list[3]['eff']*100], 
                       fmt='o', linestyle='-', label='Region 3', color='#CC79A7') ## pink
    
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

    # 두 번째 y축 생성 (twinx를 사용해 ax1과 x축을 공유)
    ax2 = ax1.twinx()
    ax2.errorbar([], [], ([], []), label="Detection efficiency", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Fake-hit rate", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')
    if (Switches[0]): ax2.errorbar(fhr_data_list[0]['vcasb'], fhr_data_list[0]['fhr'], 
                 yerr=[fhr_data_list[0]['fhr_err_low'], fhr_data_list[0]['fhr_err_up']], 
                 fmt='o', linestyle='--', mfc='none', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax2.errorbar(fhr_data_list[1]['vcasb'], fhr_data_list[1]['fhr'], 
                 yerr=[fhr_data_list[1]['fhr_err_low'], fhr_data_list[1]['fhr_err_up']], 
                 fmt='o', linestyle='--', mfc='none', label='Region 1', color='#E69F00')
    if (Switches[2]): ax2.errorbar(fhr_data_list[2]['vcasb'], fhr_data_list[2]['fhr'], 
                 yerr=[fhr_data_list[2]['fhr_err_low'], fhr_data_list[2]['fhr_err_up']], 
                 fmt='o', linestyle='--', mfc='none', label='Region 2', color='#009E73')
    if (Switches[3]): ax2.errorbar(fhr_data_list[3]['vcasb'], fhr_data_list[3]['fhr'], 
                 yerr=[fhr_data_list[3]['fhr_err_low'], fhr_data_list[3]['fhr_err_up']], 
                 fmt='o', linestyle='--', mfc='none', label='Region 3', color='#CC79A7')

    ax2.set_ylabel('Fake-hit rate [hits/pixel/event]')
    ax2.tick_params(axis='y')  
    ax2.set_ylim(0, 1e-1) #era -3
    ax2.set_yscale('symlog',linthresh=1e-10, linscale=0.90)
    ax2.set_yticks([0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])

    ax2.axhline(y=1e-6, color='grey', linestyle=':')
    ax2.text(ax2.get_xlim()[1]*0.99, 1e-6*1.70, "FHR measurement sensitivity limit", fontsize=9, color='grey', ha='right', va='top')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)
  
    print("Trying to Get_descriptions for legend")
    title_line = Get_title(CHIPNAME)
    lines = Get_descriptions(Halfunit, CHIPNAME)
    multiline_text_legend = "\n".join(lines)
    mask_line = Get_mask_info(Halfunit, CHIPNAME)
    plot_date = str(date.today().day) + ' ' + datetime.now().strftime("%b") + ' ' + str(date.today().year)
    lines_beam = [
        r'$\bf{ALICE}$ $\bf{ITS3}$ beam test $\it{WIP}$',
        '@ CERN PS Sep 2024',
        r'10 GeV/$\it{c}$ hadrons',
        'Plotted on {}'.format(plot_date),
    ]
    multiline_text_beam = "\n".join(lines_beam)

    fig.text(1.13, 0.97, f'{title_line}', fontweight='bold', transform=ax1.transAxes)
    fig.text(1.13, 0.94, multiline_text_legend.strip(), verticalalignment='top', horizontalalignment='left', transform=ax1.transAxes)
    fig.text(0.01, 0.955, multiline_text_beam.strip(), fontsize=13, ha='left', va='top',transform=ax1.transAxes)
    fig.text(0.01, 0.025, f'{mask_line}', fontsize=9, color='black', ha='left', va='center', transform=ax1.transAxes)
    print("Completed Get_descriptions for legend")

    # add_fhr_limit(ax2, 1.0/(1e+5*num_pixels_top**2))

    pathname = f"{base_paths[CHIPNAME][Halfunit]}"%(output_dir_local, 7) ## 7 is a random number
    print(pathname)
    pattern = r"/region7"
    dirname = re.sub(pattern, '', pathname)
    print(dirname)

    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_VCASB-vs-eff-and-fhr.png')
    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_VCASB-vs-eff-and-fhr.pdf')


    fig, ax1 = plt.subplots(figsize=(15.2, 7))
    plt.subplots_adjust(left=0.08, right=0.70, bottom=0.10, top=0.95)

    if (Switches[0]): ax1.errorbar(thr_data_list[0]['avg_thr'][::-1], beam_data_list[0]['eff'][::-1]*100, 
                 yerr=[(beam_data_list[0]['eff_errlow'][::-1]/beam_data_list[0]['eff'][::-1])*beam_data_list[0]['eff'][::-1]*100, 
                       (beam_data_list[0]['eff_errup'][::-1]/beam_data_list[0]['eff'][::-1])*beam_data_list[0]['eff'][::-1]*100], 
                       fmt='o', linestyle='-', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax1.errorbar(thr_data_list[1]['avg_thr'][::-1], beam_data_list[1]['eff'][::-1]*100, 
                 yerr=[(beam_data_list[1]['eff_errlow'][::-1]/beam_data_list[1]['eff'][::-1])*beam_data_list[1]['eff'][::-1]*100, 
                       (beam_data_list[1]['eff_errup'][::-1]/beam_data_list[1]['eff'][::-1])*beam_data_list[1]['eff'][::-1]*100], 
                       fmt='o', linestyle='-', label='Region 1', color='#E69F00')
    if (Switches[2]): ax1.errorbar(thr_data_list[2]['avg_thr'][::-1], beam_data_list[2]['eff'][::-1]*100, 
                 yerr=[(beam_data_list[2]['eff_errlow'][::-1]/beam_data_list[2]['eff'][::-1])*beam_data_list[2]['eff'][::-1]*100, 
                       (beam_data_list[2]['eff_errup'][::-1]/beam_data_list[2]['eff'][::-1])*beam_data_list[2]['eff'][::-1]*100], 
                       fmt='o', linestyle='-', label='Region 2', color='#009E73')
    if (Switches[3]): ax1.errorbar(thr_data_list[3]['avg_thr'][::-1], beam_data_list[3]['eff'][::-1]*100, 
                 yerr=[(beam_data_list[3]['eff_errlow'][::-1]/beam_data_list[3]['eff'][::-1])*beam_data_list[3]['eff'][::-1]*100, 
                       (beam_data_list[3]['eff_errup'][::-1]/beam_data_list[3]['eff'][::-1])*beam_data_list[3]['eff'][::-1]*100], 
                       fmt='o', linestyle='-', label='Region 3', color='#CC79A7')
    
    ax1.grid()
    ax1.set_xlabel('Threshold [DAC]')
    ax1.set_ylabel('Detection Efficiency [%]')

    ax1.tick_params(axis='y')
    ax1.set_ylim(91,101)
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 11)) 

    ax1.axhline(y=99.0, color='grey', linestyle='--')

    # 두 번째 y축 생성 (twinx를 사용해 ax1과 x축을 공유)
    ax2 = ax1.twinx()
    ax2.errorbar([], [], ([], []), label="Detection efficiency", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Fake-hit rate", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')
    if (Switches[0]): ax2.errorbar(thr_data_list[0]['avg_thr'][::-1], fhr_data_list[0]['fhr'][::-1], 
                 yerr=[fhr_data_list[0]['fhr_err_low'][::-1], fhr_data_list[0]['fhr_err_up'][::-1]], 
                 fmt='o', linestyle='--', mfc='none', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax2.errorbar(thr_data_list[1]['avg_thr'][::-1], fhr_data_list[1]['fhr'][::-1], 
                 yerr=[fhr_data_list[1]['fhr_err_low'][::-1], fhr_data_list[1]['fhr_err_up'][::-1]], 
                 fmt='o', linestyle='--', mfc='none', label='Region 1', color='#E69F00')
    if (Switches[2]): ax2.errorbar(thr_data_list[2]['avg_thr'][::-1], fhr_data_list[2]['fhr'][::-1], 
                 yerr=[fhr_data_list[2]['fhr_err_low'][::-1], fhr_data_list[2]['fhr_err_up'][::-1]], 
                 fmt='o', linestyle='--', mfc='none', label='Region 2', color='#009E73')
    if (Switches[3]): ax2.errorbar(thr_data_list[3]['avg_thr'][::-1], fhr_data_list[3]['fhr'][::-1], 
                 yerr=[fhr_data_list[3]['fhr_err_low'][::-1], fhr_data_list[3]['fhr_err_up'][::-1]], 
                 fmt='o', linestyle='--', mfc='none', label='Region 3', color='#CC79A7')

    ax2.set_ylabel('Fake-hit rate [hits/pixel/event]')
    ax2.tick_params(axis='y')  
    ax2.set_ylim(0, 1e-1) #era -3
    ax2.set_yscale('symlog',linthresh=1e-10, linscale=0.90)
    ax2.set_yticks([0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])

    ax2.axhline(y=1e-6, color='grey', linestyle=':')
    ax2.text(ax2.get_xlim()[1]*0.99, 1e-6*1.70, "FHR measurement sensitivity limit", fontsize=9, color='grey', ha='right', va='top')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)

    print("Trying to Get_descriptions for legend")
    fig.text(1.13, 0.97, f'{title_line}', fontweight='bold', transform=ax1.transAxes)
    fig.text(1.13, 0.94, multiline_text_legend.strip(), verticalalignment='top', horizontalalignment='left', transform=ax1.transAxes)
    fig.text(0.01, 0.955, multiline_text_beam.strip(), fontsize=13, ha='left', va='top',transform=ax1.transAxes)
    fig.text(0.01, 0.025, f'{mask_line}', fontsize=9, color='black', ha='left', va='center', transform=ax1.transAxes)
    print("Completed Get_descriptions for legend")

    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_THR-vs-eff-and-fhr.png')
    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_THR-vs-eff-and-fhr.pdf')


    # ################################################################## Spatial resolution and cluster size

    # Figure와 첫 번째 Axes 생성
    fig, ax1 = plt.subplots(figsize=(15.2, 7))
    plt.subplots_adjust(left=0.08, right=0.70, bottom=0.10, top=0.95)

    # 첫 번째 y축에 대한 데이터 플롯
    if (Switches[0]): ax1.errorbar(spa_data_list[0]['vcasb'], spa_data_list[0]['spatial_res_mean'], yerr=spa_data_list[0]['spatial_res_uncert'], 
                 fmt='o', linestyle='-', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax1.errorbar(spa_data_list[1]['vcasb'], spa_data_list[1]['spatial_res_mean'], yerr=spa_data_list[1]['spatial_res_uncert'], 
                 fmt='o', linestyle='-', label='Region 1', color='#E69F00')
    if (Switches[2]): ax1.errorbar(spa_data_list[2]['vcasb'], spa_data_list[2]['spatial_res_mean'], yerr=spa_data_list[2]['spatial_res_uncert'], 
                 fmt='o', linestyle='-', label='Region 2', color='#009E73')
    if (Switches[3]): ax1.errorbar(spa_data_list[3]['vcasb'], spa_data_list[3]['spatial_res_mean'], yerr=spa_data_list[3]['spatial_res_uncert'], 
                 fmt='o', linestyle='-', label='Region 3', color='#CC79A7')
    ax1.grid()
    ax1.set_xlabel(r'$\it{V_{casb}}$ [DAC]')
    ax1.set_ylabel('Spatial resolution [\u03BCm]')
    ax1.tick_params(axis='y')

    # 두 번째 y축 생성 (twinx를 사용해 ax1과 x축을 공유)
    ax2 = ax1.twinx()
    ax2.errorbar([], [], ([], []), label="Spatial resolution", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Cluster size", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')
    if (Switches[0]): ax2.errorbar(beam_data_list[0]['vcasb'], beam_data_list[0]['cluSize'], yerr=beam_data_list[0]['cluSize_err'], 
                 fmt='o', linestyle='--', mfc='none', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax2.errorbar(beam_data_list[1]['vcasb'], beam_data_list[1]['cluSize'], yerr=beam_data_list[1]['cluSize_err'], 
                 fmt='o', linestyle='--', mfc='none', label='Region 1', color='#E69F00')
    if (Switches[2]): ax2.errorbar(beam_data_list[2]['vcasb'], beam_data_list[2]['cluSize'], yerr=beam_data_list[2]['cluSize_err'], 
                 fmt='o', linestyle='--', mfc='none', label='Region 2', color='#009E73')
    if (Switches[3]): ax2.errorbar(beam_data_list[3]['vcasb'], beam_data_list[3]['cluSize'], yerr=beam_data_list[3]['cluSize_err'], 
                 fmt='o', linestyle='--', mfc='none', label='Region 3', color='#CC79A7')

    ax2.set_ylabel('Average cluster size [pixels]')
    ax2.tick_params(axis='y') 
    # ax2.set_ylim(91,101) 
    # ax1.set_ylim(91,101)
    # ax1.set_xlim(45,130)
    # ax1.axhline(y=99.0, color='grey', linestyle='--')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)

    print("Trying to Get_descriptions for legend")
    fig.text(1.13, 0.97, f'{title_line}', fontweight='bold', transform=ax1.transAxes)
    fig.text(1.13, 0.94, multiline_text_legend.strip(), verticalalignment='top', horizontalalignment='left', transform=ax1.transAxes)
    fig.text(0.01, 0.955, multiline_text_beam.strip(), fontsize=13, ha='left', va='top',transform=ax1.transAxes)
    fig.text(0.01, 0.025, f'{mask_line}', fontsize=9, color='black', ha='left', va='center', transform=ax1.transAxes)
    print("Completed Get_descriptions for legend")

    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_VCASB-vs-resol-and-clust.png')
    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_VCASB-vs-resol-and-clust.pdf')


    fig, ax1 = plt.subplots(figsize=(15.2, 7))
    plt.subplots_adjust(left=0.08, right=0.70, bottom=0.10, top=0.95)
    if (Switches[0]): ax1.errorbar(thr_data_list[0]['avg_thr'][::-1], spa_data_list[0]['spatial_res_mean'][::-1], yerr=spa_data_list[0]['spatial_res_uncert'][::-1], 
                 fmt='o', linestyle='-', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax1.errorbar(thr_data_list[1]['avg_thr'][::-1], spa_data_list[1]['spatial_res_mean'][::-1], yerr=spa_data_list[1]['spatial_res_uncert'][::-1], 
                 fmt='o', linestyle='-', label='Region 1', color='#E69F00')
    if (Switches[2]): ax1.errorbar(thr_data_list[2]['avg_thr'][::-1], spa_data_list[2]['spatial_res_mean'][::-1], yerr=spa_data_list[2]['spatial_res_uncert'][::-1], 
                 fmt='o', linestyle='-', label='Region 2', color='#009E73')
    if (Switches[3]): ax1.errorbar(thr_data_list[3]['avg_thr'][::-1], spa_data_list[3]['spatial_res_mean'][::-1], yerr=spa_data_list[3]['spatial_res_uncert'][::-1], 
                 fmt='o', linestyle='-', label='Region 3', color='#CC79A7')
    ax1.grid()
    ax1.set_xlabel('Threshold [DAC]')
    ax1.set_ylabel('Spatial resolution [\u03BCm]')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.errorbar([], [], ([], []), label="Spatial resolution", marker='s', linestyle='-', elinewidth=1.3, capsize=1.5, color='dimgrey')
    ax2.errorbar([], [], ([], []), label="Cluster size", marker='s', markerfacecolor='none', linestyle='--', elinewidth=1.3, capsize=1.5, color='dimgrey')
    if (Switches[0]): ax2.errorbar(thr_data_list[0]['avg_thr'][::-1], beam_data_list[0]['cluSize'][::-1], yerr=beam_data_list[0]['cluSize_err'][::-1], 
                 fmt='o', linestyle='--', mfc='none', label='Region 0', color='#56B4E9')
    if (Switches[1]): ax2.errorbar(thr_data_list[1]['avg_thr'][::-1], beam_data_list[1]['cluSize'][::-1], yerr=beam_data_list[1]['cluSize_err'][::-1], 
                 fmt='o', linestyle='--', mfc='none', label='Region 1', color='#E69F00')
    if (Switches[2]): ax2.errorbar(thr_data_list[2]['avg_thr'][::-1], beam_data_list[2]['cluSize'][::-1], yerr=beam_data_list[2]['cluSize_err'][::-1], 
                 fmt='o', linestyle='--', mfc='none', label='Region 2', color='#009E73')
    if (Switches[3]): ax2.errorbar(thr_data_list[3]['avg_thr'][::-1], beam_data_list[3]['cluSize'][::-1], yerr=beam_data_list[3]['cluSize_err'][::-1], 
                 fmt='o', linestyle='--', mfc='none', label='Region 3', color='#CC79A7')

    ax2.set_ylabel('Average cluster size [pixels]')
    ax2.tick_params(axis='y') 
    # ax2.set_ylim(91,101) 
    # ax1.set_ylim(91,101)
    # ax1.set_xlim(45,130)
    # ax1.axhline(y=99.0, color='grey', linestyle='--')
    ax2.legend(bbox_to_anchor=(1.15, 0), loc='lower left', borderaxespad=0.)

    print("Trying to Get_descriptions for legend")
    fig.text(1.13, 0.97, f'{title_line}', fontweight='bold', transform=ax1.transAxes)
    fig.text(1.13, 0.94, multiline_text_legend.strip(), verticalalignment='top', horizontalalignment='left', transform=ax1.transAxes)
    fig.text(0.01, 0.955, multiline_text_beam.strip(), fontsize=13, ha='left', va='top',transform=ax1.transAxes)
    fig.text(0.01, 0.025, f'{mask_line}', fontsize=9, color='black', ha='left', va='center', transform=ax1.transAxes)
    print("Completed Get_descriptions for legend")

    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_THR-vs-resol-and-clust.png')
    plt.savefig(f'{dirname}/{CHIPNAME}_{Halfunit}_THR-vs-resol-and-clust.pdf')

    os.system(f'ls {dirname}')
    plt.show()

    print("=============================")

    print(beam_data_list[2].columns)
    print( thr_data_list[2].columns)
    print( fhr_data_list[2].columns)
    print( spa_data_list[2].columns)

    for i in Switches_list:
        csv_file = pd.DataFrame({
            'half_unit': thr_data_list[i]['halfunit'],
            'region': thr_data_list[i]['region'],
            'vcasb': beam_data_list[i]['vcasb'],
            'eff': beam_data_list[i]['eff'],
            'eff_err_low': beam_data_list[i]['eff_errlow'],
            'eff_err_up': beam_data_list[i]['eff_errup'],
            'thr': thr_data_list[i]['avg_thr'],
            'fhr': fhr_data_list[i]['fhr'],
            'fhr_err_low': fhr_data_list[i]['fhr_err_up'],
            'fhr_err_up': fhr_data_list[i]['fhr_err_low'],
            'spatial_res': spa_data_list[i]['spatial_res_mean'],
            'spatial_res_err': spa_data_list[i]['spatial_res_uncert'],
            'cluster_size': beam_data_list[i]['cluSize'],
            'cluster_size_err': beam_data_list[i]['cluSize_err'],
            'vcasb_thr': thr_data_list[i]['vcasb'],
            'vcasb_fhr': fhr_data_list[i]['vcasb'],
        })

        csv_file.to_csv(f'{dirname}/{CHIPNAME}_{Halfunit}_reg{i}_data.csv')
        print(csv_file.head())
 

    input()



def Get_Spatial_Resolution(beam_data_list):

    print(beam_data_list.columns)
    print(beam_data_list['reg_num'][0])

    region_num = beam_data_list['reg_num'][0]
    if region_num == 0 or region_num == 3:
        trk_res = 4.66
    elif region_num == 1 or region_num == 2:
        trk_res = 2.18
    else:
        print("non sence region number in Get_Spatial_Resolution")
        sys.exit(1)
    print("trk_res : ", trk_res)
    trk_uncert = 0.41

    vcasb_list =[]
    spatial_res_mean_list = []
    spatial_res_uncert_list = []


    for index, value in enumerate(beam_data_list['vcasb']):
        res_x = beam_data_list['resX'][index]
        res_y = beam_data_list['resY'][index]
        res_x_err = beam_data_list['resX_err'][index]
        res_y_err = beam_data_list['resY_err'][index]

        vcasb_list.append(value)
        spatial_resX = np.sqrt(res_x**2 - trk_res**2)
        spatial_resY = np.sqrt(res_y**2 - trk_res**2)
        spatial_res_mean = (spatial_resX + spatial_resY)/2
        spatial_res_mean_list.append(spatial_res_mean)

        # print(index, value, spatial_resX)
        # print(index, value, spatial_resY)

        if region_num == 0 or region_num == 3:
            spatial_uncert_x = np.sqrt((res_x/spatial_resX)**2 *(res_x_err)**2 + (trk_res/spatial_resX)**2 *(trk_uncert)**2)
            spatial_uncert_y = np.sqrt((res_y/spatial_resY)**2 *(res_y_err)**2 + (trk_res/spatial_resY)**2 *(trk_uncert)**2)
        elif region_num == 1 or region_num == 2:
            spatial_uncert_x = (res_x/spatial_resX)*res_x_err
            spatial_uncert_y = (res_y/spatial_resY)*res_y_err

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


def Load_FHR_THR_files(fhr_data_list, thr_data_list, Halfunit, CHIPNAME):


    if CHIPNAME == "babyMOSS-2_3_W02F4":

        path_common = "/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/data/2024-08_PS_II/MOSS_TEST_RESULTS"

        if Halfunit == "tb":
            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_193929_tb_reg0/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_194358_tb_reg1/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_194818_tb_reg2/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_195244_tb_reg3/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_193929_tb_reg0/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_194358_tb_reg1/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_194818_tb_reg2/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_195244_tb_reg3/summary_thr.csv'))
    
        elif Halfunit == "bb":
            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_204043_bb_reg0/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_204504_bb_reg1/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_204927_bb_reg2/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/FakeHitRateScan/ScanCollection_20240819_205349_bb_reg3/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_204043_bb_reg0/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_204504_bb_reg1/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_204927_bb_reg2/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-2_3_W02F4/ThresholdScan/ScanCollection_20240819_205349_bb_reg3/summary_thr.csv'))

    elif CHIPNAME == "babyMOSS-4_4_W21D4":

        path_common = "/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/data/2024-09_PS/MOSS_TEST_RESULTS"

        if Halfunit == "tb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/FakeHitRateScan/ScanCollection_20240906_161100_tb_reg0/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/FakeHitRateScan/ScanCollection_20240906_161546_tb_reg1/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/FakeHitRateScan/ScanCollection_20240906_162032_tb_reg2/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/FakeHitRateScan/ScanCollection_20240906_162517_tb_reg3/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/ThresholdScan/ScanCollection_20240906_161100_tb_reg0/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/ThresholdScan/ScanCollection_20240906_161546_tb_reg1/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/ThresholdScan/ScanCollection_20240906_162032_tb_reg2/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/ThresholdScan/ScanCollection_20240906_162517_tb_reg3/summary_thr.csv'))
    
        elif Halfunit == "bb":
            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/FakeHitRateScan/ScanCollection_20240906_153920_bb_reg0/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/FakeHitRateScan/ScanCollection_20240906_155358_bb_reg3/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/ThresholdScan/ScanCollection_20240906_153920_bb_reg0/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/babyMOSS-4_4_W21D4/ThresholdScan/ScanCollection_20240906_155358_bb_reg3/summary_thr.csv'))

    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias62":

        path_common = "/home/jiyoung/AnalysisData/2024-05_PS/thr_fhr_scans/babyMOSS-5_2_W24B5"

        if Halfunit == "tb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_62/region_0/ScanCollection_20240518_083717/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_62/region_1/ScanCollection_20240518_084255/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_62/region_2/ScanCollection_20240518_085031/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_62/region_3/ScanCollection_20240518_085556/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_62/region_0/ScanCollection_20240518_083717/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_62/region_1/ScanCollection_20240518_084255/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_62/region_2/ScanCollection_20240518_085031/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_62/region_3/ScanCollection_20240518_085556/summary_thr.csv'))
    
        elif Halfunit == "bb":

            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/bottom/psub_12/ibias_62/region_1/ScanCollection_20240518_080309/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/bottom/psub_12/ibias_62/region_2/ScanCollection_20240518_080832/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/bottom/psub_12/ibias_62/region_3/ScanCollection_20240518_081334/summary_masked.csv'))

            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/bottom/psub_12/ibias_62/region_1/ScanCollection_20240518_080309/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/bottom/psub_12/ibias_62/region_2/ScanCollection_20240518_080832/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/bottom/psub_12/ibias_62/region_3/ScanCollection_20240518_081334/summary_thr.csv'))


    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias124":

        path_common = "/home/jiyoung/AnalysisData/2024-05_PS/thr_fhr_scans/babyMOSS-5_2_W24B5"

        if Halfunit == "tb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_124/region_0/ScanCollection_20240518_090133/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_124/region_1/ScanCollection_20240518_090659/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_124/region_2/ScanCollection_20240518_091205/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/top/psub_12/ibias_124/region_3/ScanCollection_20240518_091713/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_124/region_0/ScanCollection_20240518_090133/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_124/region_1/ScanCollection_20240518_090659/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_124/region_2/ScanCollection_20240518_091205/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/top/psub_12/ibias_124/region_3/ScanCollection_20240518_091713/summary_thr.csv'))
    
        elif Halfunit == "bb":

            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/bottom/psub_12/ibias_62/region_1/ScanCollection_20240518_080309/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/bottom/psub_12/ibias_62/region_2/ScanCollection_20240518_080832/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/bottom/psub_12/ibias_62/region_3/ScanCollection_20240518_081334/summary_masked.csv'))

            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/bottom/psub_12/ibias_124/region_1/ScanCollection_20240518_082013/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/bottom/psub_12/ibias_124/region_2/ScanCollection_20240518_082523/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/bottom/psub_12/ibias_124/region_3/ScanCollection_20240518_083028/summary_thr.csv'))


    elif CHIPNAME == "MOSS-5_W24B5_ibias62":

        path_common = "/home/jiyoung/AnalysisData/2024-05_PS/thr_fhr_scans/MOSS-5_W24B5"

        if Halfunit == "tb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_62/region_0/ScanCollection_20240513_143034/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_62/region_1/ScanCollection_20240513_144659/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_62/region_2/ScanCollection_20240513_145607/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_62/region_3/ScanCollection_20240513_150516/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_62/region_0/ScanCollection_20240513_143034/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_62/region_1/ScanCollection_20240513_144659/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_62/region_2/ScanCollection_20240513_145607/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_62/region_3/ScanCollection_20240513_150516/summary_thr.csv'))

        elif Halfunit == "bb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_62/region_0/ScanCollection_20240516_111215/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_62/region_1/ScanCollection_20240516_112227/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_62/region_2/ScanCollection_20240516_112903/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_62/region_3/ScanCollection_20240516_113755/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_62/region_0/ScanCollection_20240516_111215/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_62/region_1/ScanCollection_20240516_112227/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_62/region_2/ScanCollection_20240516_112903/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_62/region_3/ScanCollection_20240516_113755/summary_thr.csv'))

    elif CHIPNAME == "MOSS-5_W24B5_ibias124":

        path_common = "/home/jiyoung/AnalysisData/2024-05_PS/thr_fhr_scans/MOSS-5_W24B5"

        if Halfunit == "tb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_124/region_0/ScanCollection_20240513_151528/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_124/region_1/ScanCollection_20240513_152459/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_124/region_2/ScanCollection_20240513_153316/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/t7/psub_12/ibias_124/region_3/ScanCollection_20240513_154045/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_124/region_0/ScanCollection_20240513_151528/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_124/region_1/ScanCollection_20240513_152459/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_124/region_2/ScanCollection_20240513_153316/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/t7/psub_12/ibias_124/region_3/ScanCollection_20240513_154045/summary_thr.csv'))

        elif Halfunit == "bb":

            fhr_data_list.insert(0, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_124/region_0/ScanCollection_20240516_114518/summary_masked.csv'))
            fhr_data_list.insert(1, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_124/region_1/ScanCollection_20240516_115106/summary_masked.csv'))
            fhr_data_list.insert(2, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_124/region_2/ScanCollection_20240516_115658/summary_masked.csv'))
            fhr_data_list.insert(3, pd.read_csv(f'{path_common}/FakeHitRateScan/b4/psub_12/ibias_124/region_3/ScanCollection_20240516_120249/summary_masked.csv'))

            thr_data_list.insert(0, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_124/region_0/ScanCollection_20240516_114518/summary_thr.csv'))
            thr_data_list.insert(1, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_124/region_1/ScanCollection_20240516_115106/summary_thr.csv'))
            thr_data_list.insert(2, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_124/region_2/ScanCollection_20240516_115658/summary_thr.csv'))
            thr_data_list.insert(3, pd.read_csv(f'{path_common}/ThresholdScan/b4/psub_12/ibias_124/region_3/ScanCollection_20240516_120249/summary_thr.csv'))

    else:
        ("Cannot find correct FHR and THR files")
        sys.exit(1)


def Get_descriptions(Halfunit, CHIPNAME):
    if CHIPNAME == "babyMOSS-2_3_W02F4" and Halfunit == "tb":
        lines = [
            "Irradiated: 10$^{13}$ 1 MeV n$_{\mathrm{eq}}$ cm$^{-2}$",
            "Wafer: W02F2?",
            "Split: 2_3?",
            "Pitch: 22.5 \u03BCm",
            "Half-unit: Top",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-2_3_W02F4" and Halfunit == "bb":
        lines = [
            "Irradiated: 10$^{13}$ 1 MeV n$_{\mathrm{eq}}$ cm$^{-2}$",
            "Wafer: W02F4",
            "Split: 2_3??",
            "Pitch: 18 \u03BCm",
            "Half-unit: Bottom",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-4_4_W21D4" and Halfunit == "tb":
        lines = [
            "Irradiated: 1 Mrad",
            "Wafer: W21D4",
            "Split: ?",
            "Pitch: 22.5 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Top",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 95 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-4_4_W21D4" and Halfunit == "bb":
        lines = [
            "Irradiated: 1 Mrad",
            "Wafer: W21D4",
            "Split: ?",
            "Pitch: 18 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Bottom",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 95 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias62" and Halfunit == "tb":
        lines = [
            "Irradiated: 10$^{13}$ 1 MeV n$_{\mathrm{eq}}$ cm$^{-2}$",
            "Wafer: W24",
            "Split: ?",
            "Pitch: 22.5 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Top",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 15 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias62" and Halfunit == "bb":
        lines = [
            "Irradiated: 10$^{13}$ 1 MeV n$_{\mathrm{eq}}$ cm$^{-2}$",
            "Wafer: W24",
            "Split: ?",
            "Pitch: 18 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Bottom",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 15 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias124" and Halfunit == "tb":
        lines = [
            "Irradiated: 10$^{13}$ 1 MeV n$_{\mathrm{eq}}$ cm$^{-2}$",
            "Wafer: W24",
            "Split: ?",
            "Pitch: 22.5 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Top",
            r"$\it{I_{bias}}$ = 124 DAC",
            r"$\it{I_{biasn}}$ = 200 DAC",
            r"$\it{I_{reset}}$ = 15 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 125 DAC",
            r"$\it{V_{casn}}$ = 110 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias124" and Halfunit == "bb":
        lines = [
            "Irradiated: 10$^{13}$ 1 MeV n$_{\mathrm{eq}}$ cm$^{-2}$",
            "Wafer: W24",
            "Split: ?",
            "Pitch: 18 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Bottom",
            r"$\it{I_{bias}}$ = 124 DAC",
            r"$\it{I_{biasn}}$ = 200 DAC",
            r"$\it{I_{reset}}$ = 15 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 125 DAC",
            r"$\it{V_{casn}}$ = 110 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "MOSS-5_W24B5_ibias62" and Halfunit == "tb":
        lines = [
            "Irradiated: Non-irradiated",
            "Wafer: ",
            "Split: ",
            "Pitch: 22.5 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Top (T7)",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "MOSS-5_W24B5_ibias62" and Halfunit == "bb":
        lines = [
            "Irradiated: Non-irradiated",
            "Wafer: ",
            "Split: ",
            "Pitch: 18 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Bottom (B4)",
            r"$\it{I_{bias}}$ = 62 DAC",
            r"$\it{I_{biasn}}$ = 100 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 145 DAC",
            r"$\it{V_{casn}}$ = 104 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "MOSS-5_W24B5_ibias124" and Halfunit == "tb":
        lines = [
            "Irradiated: Non-irradiated",
            "Wafer: ",
            "Split: ",
            "Pitch: 22.5 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Top (T7)",
            r"$\it{I_{bias}}$ = 124 DAC",
            r"$\it{I_{biasn}}$ = 200 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 125 DAC",
            r"$\it{V_{casn}}$ = 110 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    elif CHIPNAME == "MOSS-5_W24B5_ibias124" and Halfunit == "bb":
        lines = [
            "Irradiated: Non-irradiated",
            "Wafer: ",
            "Split: ",
            "Pitch: 18 \u03BCm",
            "Ngap:  5 \u03BCm",
            "Half-unit: Bottom (B4)",
            r"$\it{I_{bias}}$ = 124 DAC",
            r"$\it{I_{biasn}}$ = 200 DAC",
            r"$\it{I_{reset}}$ = 10 DAC",
            r"$\it{I_{db}}$ = 50 DAC",
            r"$\it{V_{shift}}$ = 125 DAC",
            r"$\it{V_{casn}}$ = 110 DAC",
            r"$\it{V_{psub}}$ = -1.2 V",
            r"$\it{V_{casb}}$ = variable",
            "Strobe length = 6.0 \u03BCs",
            "T = 27 \u00B0C",
        ]
    else:
        ("Cannot find a correct discription")
        sys.exit(1)

    return lines

def Get_title(CHIPNAME):

    if CHIPNAME == "babyMOSS-2_3_W04E2":
        title = 'babyMOSS-2_3_W04E2'
    elif CHIPNAME == "babyMOSS-2_3_W02F4":
        title = 'babyMOSS-2_3_W02F4'
    elif CHIPNAME == "babyMOSS-4_4_W21D4":
        title = 'babyMOSS-4_4_W21D4'    
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias62" or CHIPNAME == "babyMOSS-5_2_W24B5_ibias124":
        title = 'babyMOSS-5_2_W24B5'
    elif CHIPNAME == "MOSS-5_W24B5_ibias62" or CHIPNAME == "MOSS-5_W24B5_ibias124":
        title = 'MOSS-5_W24B5'    
    else:
        ("Cannot find a correct title")
        sys.exit(1)

    return title

def Get_mask_info(Halfunit, CHIPNAME):

    if CHIPNAME == "babyMOSS-2_3_W02F4" and Halfunit == "tb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (0, 0, 0, 0)"
    elif CHIPNAME == "babyMOSS-2_3_W02F4" and Halfunit == "bb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (0, x, x, 0)"

    elif CHIPNAME == "babyMOSS-4_4_W21D4" and Halfunit == "tb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (2, 0, 1, 2)"
    elif CHIPNAME == "babyMOSS-4_4_W21D4" and Halfunit == "bb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (0, x, x, 0)"

    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias62" and Halfunit == "tb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (x, 0, 1, 0)"
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias62" and Halfunit == "bb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (x, 0, 1, 1)"

    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias124" and Halfunit == "tb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (x, 0, 1, 0)"
    elif CHIPNAME == "babyMOSS-5_2_W24B5_ibias124" and Halfunit == "bb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (x, 0, 1, 4)"

    elif CHIPNAME == "MOSS-5_W24B5_ibias62" and Halfunit == "tb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (0, 0, 0, 0)"
    elif CHIPNAME == "MOSS-5_W24B5_ibias62" and Halfunit == "bb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (1, 0, 0, 1)"

    elif CHIPNAME == "MOSS-5_W24B5_ibias124" and Halfunit == "tb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (0, 0, 0, 0)"
    elif CHIPNAME == "MOSS-5_W24B5_ibias124" and Halfunit == "bb":
        info = "Association window: 100 \u03BCm. Masked pixels per region: (0, 0, 0, 1)"

    else:
        ("Cannot find a correct mask info")
        sys.exit(1)

    return info


if __name__ == "__main__":
    main(sys.argv)





