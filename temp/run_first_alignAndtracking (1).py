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

    CHIP_TYPE = "babyMOSS" ## "babyMOSS" or "MOSS"
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
        # # 1: list(range(82, 109, 3)), ## ver2, 82 - 106
        # 2: list(range(88, 124, 3)), ## exclude 124 too noisy
        # 3: list(range(79, 115, 3)), ## exclude 115 too noisy

        ## for bb (b4)
        # 0: list(range(86, 125, 3)),
        # 1: list(range(86, 122, 3)), 
        # 2: list(range(86, 113, 3)), ## 86 - 110
        # 3: list(range(70, 115, 3)), ## exclude 115 too noisy

        # ## for baby-5_2_W24B5, for ibias 62
        # # tb
        1: list(range(76, 115, 3)),
        2: list(range(85, 124, 3)), 
        3: list(range(77, 116, 3)),
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

        # ## baby-2_3_W02F4
        # ## tb
        # 0: list(range(72, 114, 3)),
        # 1: list(range(69, 111, 3)),
        # 2: list(range(77, 119, 3)),
        # 3: list(range(70, 112, 3)),

        # # ## bb
        # 0: list(range(69, 111, 3)),
        # 1: list(range(69, 111, 3)), - no. to check (lack of statistics)
        # 3: list(range(65, 107, 3)), 


    }

    if region_number not in base_vcasb_collection:
        print(f"Out of range: region number {region_number}")
        sys.exit(1)

    vcasb_List = base_vcasb_collection[region_number]
    print(vcasb_List)

    run_list = [  

        # # ## baby-5_2_W24B5, ibias 62
        # # ## tb (reg1)
        # "run206102947_240518102954.raw",
        # "run206102948_240518105812.raw",
        # "run206102949_240518112140.raw",
        # "run206102950_240518113840.raw",
        # "run206102951_240518115600.raw",
        # "run206102952_240518121317.raw",
        # "run206102953_240518123034.raw",
        # "run206102954_240518124751.raw",
        # "run206102955_240518130505.raw",
        # "run206102956_240518132223.raw",
        # "run206102957_240518133940.raw",
        # "run206102958_240518135627.raw",
        # "run206102959_240518142339.raw",

        # # ## tb (reg2)
        # "run206102960_240518145151.raw",
        # "run206102961_240518151959.raw",
        # "run206102962_240518153806.raw",
        # "run206102963_240518155524.raw",
        # "run206102964_240518161241.raw",
        # "run206102965_240518162928.raw",
        # "run206102966_240518164628.raw",
        # "run206102967_240518170347.raw",
        # "run206102968_240518172104.raw",
        # "run206102969_240518173821.raw",
        # "run206102970_240518175539.raw",
        # "run206102971_240518181256.raw",
        # "run206102972_240518183013.raw",

        # # ## tb (reg3)
        # "run206102973_240518184730.raw",
        # "run206102974_240518190444.raw",
        # "run206102975_240518192203.raw",
        # "run206102976_240518193920.raw",
        # "run206102977_240518195637.raw",
        # "run206102978_240518201354.raw",
        # "run206102979_240518203111.raw",
        # "run206102980_240518204755.raw",
        # "run206102981_240518210456.raw",
        # "run206102982_240518212213.raw",
        # "run206102983_240518215025.raw",
        # "run206102984_240518221836.raw",
        # "run206102985_240518224724.raw",

        # # # ## baby-5_2_W24B5, ibias 124
        # # # ## tb (reg0)
        # "run206102986_240518231132.raw",
        # "run206102987_240518232432.raw",
        # "run206102988_240518233759.raw",
        # "run206102989_240518235126.raw",
        # "run206102990_240519000443.raw",
        # "run206102991_240519001750.raw",
        # "run206102992_240519003117.raw",
        # "run206102993_240519004439.raw",
        # "run206102994_240519005753.raw",
        # "run206102995_240519011100.raw",
        # "run206102996_240519012427.raw",
        # "run206102997_240519013735.raw",
        # "run206102998_240519015102.raw",

        # # # ## tb (reg1)
        # "run206102999_240519020539.raw",
        # "run206103000_240519021906.raw",
        # "run206103001_240519023233.raw",
        # "run206103002_240519024540.raw",
        # "run206103003_240519025847.raw",
        # "run206103004_240519031214.raw",
        # "run206103005_240519032542.raw",
        # "run206103006_240519033849.raw",
        # "run206103007_240519035217.raw",
        # "run206103008_240519040544.raw",
        # "run206103009_240519041856.raw",
        # "run206103010_240519043450.raw",
        # "run206103011_240519044816.raw",

        # # # ## tb (reg2)
        # "run206103012_240519050143.raw",
        # "run206103013_240519052915.raw",
        # "run206103014_240519055725.raw",
        # "run206103015_240519062503.raw",
        # "run206103016_240519065315.raw",
        # "run206103017_240519072053.raw",
        # "run206103018_240519074831.raw",
        # "run206103019_240519081639.raw",
        # "run206103020_240519094231.raw",
        # "run206103021_240519101008.raw",
        # "run206103022_240519103817.raw",
        # "run206103023_240519110629.raw",
        # "run206103024_240519113441.raw",

        # # # ## tb (reg3)
        # "run206103025_240519120328.raw",
        # "run206103026_240519123139.raw",
        # "run206103027_240519125852.raw",
        # "run206103028_240519131612.raw",
        # "run206103029_240519133945.raw",
        # "run206103030_240519140756.raw",
        # "run206103031_240519143204.raw",
        # "run206103032_240519144951.raw",
        # "run206103033_240519150709.raw",
        # "run206103034_240519152426.raw",
        # "run206103035_240519154144.raw",
        # "run206103036_240519155901.raw",
        # "run206103037_240519161618.raw",

    ]

    if not len(run_list) == len(vcasb_List):
        print(f"Lengths of Run list and vcasb list are not matched! Please check it!")
        sys.exit(1)

    # 함수를 사용하여 새로운 딕셔너리 생성
    first_elements_dict = extract_first_elements(base_vcasb_collection)

    # 결과 출력
    print(first_elements_dict)

    data_dir_local = "/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/data"
    base_paths = {
        'babyMOSS-2_3_W04E2': {
            'tb': '%s/2024-08_PS_II/babyMOSS-2_3_W04E2/tb_psub12/region%d/VCASB%d/%s',
            'bb': '%s/2024-08_PS_II/babyMOSS-2_3_W04E2/bb_psub12/region%d/VCASB%d/%s',
        },
        'babyMOSS-2_3_W02F4': {
            'tb': '%s/2024-08_PS_II/babyMOSS-2_3_W02F4/tb_psub12/region%d/VCASB%d/%s',
            'bb': '%s/2024-08_PS_II/babyMOSS-2_3_W02F4/bb_psub12/region%d/VCASB%d/%s',
        },
        'babyMOSS-4_4_W21D4': {
            'tb': '%s/2024-09_PS/babyMOSS-4_4_W21D4/tb_psub12/region%d/VCASB%d/%s',
            'bb': '%s/2024-09_PS/babyMOSS-4_4_W21D4/bb_psub12/region%d/VCASB%d/%s',
        },
        'babyMOSS-5_2_W24B5_ibias62': {
            'tb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/top/psub_12/ibias_62/region_%d/VCASB_%d/%s',
            'bb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/bottom/psub_12/ibias_62/region_%d/VCASB_%d/%s',
        },
        'babyMOSS-5_2_W24B5_ibias124': {
            'tb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/top/psub_12/ibias_124/region_%d/VCASB_%d/%s',
            'bb': '%s/2024-05_PS/babyMOSS-5_2_W24B5/bottom/psub_12/ibias_124/region_%d/VCASB_%d/%s',
        },
        'MOSS-5_W24B5_ibias62': {
            'tb': '%s/2024-05_PS/MOSS-5_W24B5/t7/psub_12/ibias_62/region_%d/VCASB_%d/%s',
            'bb': '%s/2024-05_PS/MOSS-5_W24B5/b4/psub_12/ibias_62/region_%d/VCASB_%d/%s',
        },
        'MOSS-5_W24B5_ibias124': {
            'tb': '%s/2024-05_PS/MOSS-5_W24B5/t7/psub_12/ibias_124/region_%d/VCASB_%d/%s',
            'bb': '%s/2024-05_PS/MOSS-5_W24B5/b4/psub_12/ibias_124/region_%d/VCASB_%d/%s',
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

    remains = glob.glob("/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/*.root")
    if not len(remains) == 0:
        print(f"Please clean up the output directory first")
        sys.exit(1)

    for index, filename in enumerate(run_list):

        OPT_FNAME = f"EventLoaderEUDAQ2.file_name={base_paths[CHIPNAME][Halfunit]}" % (data_dir_local, region_number, vcasb_List[index], filename)

        if Halfunit == "tb":
            SIDE = "top"
        elif Halfunit == "bb":
            SIDE = "bot"

        print(OPT_FNAME)
        print(SIDE)
        
        pathname = "/".join(OPT_FNAME.split("/")[1:])
        # 해당 경로가 존재하는지 확인
        if not os.path.exists(f'/{pathname}'):
            print(f"Error: The specified path does not exist: /{pathname}")
            sys.exit(1)  # 오류 코드 1과 함께 프로그램 종료

        os.system("rm output.txt")
        with open('output.txt', 'a') as log:  # 'a' 모드로 파일 열기 (추가모드 add)

            highestTHR = check_highest_threshold(first_elements_dict, region_number, vcasb_List[index])

            if highestTHR == "y":
                print("Mask creation + Prealign + ALPIDE-align + DUT-align")
                
                ## Mask creation
                # create_mask(OPT_FNAME, CHIPNAME, Halfunit, SIDE, log, CHIP_TYPE)
            
                ## Pre-alignment step
                pre_alignment(OPT_FNAME, CHIPNAME, Halfunit, log, CHIP_TYPE)

                ## Alignment step (only ALPIDE alignment)
                ALPIDE_alignment(OPT_FNAME, CHIPNAME, Halfunit, log, CHIP_TYPE)

                ## Alignment step including DUT
                DUT_alignment(OPT_FNAME, CHIPNAME, Halfunit, region_number, log, CHIP_TYPE)
                # DUT_alignment(OPT_FNAME, CHIPNAME, 0, log)
                # DUT_alignment(OPT_FNAME, CHIPNAME, 1, log)
                # DUT_alignment(OPT_FNAME, CHIPNAME, 2, log)
                # DUT_alignment(OPT_FNAME, CHIPNAME, 3, log)
            else:
                print("Skipping mask creation.")

            ## Analysis step (separately proceed with each 4 region in MOSS-Half Unit)
            Analysis(OPT_FNAME, CHIPNAME, Halfunit, region_number, log, CHIP_TYPE)
            # Analysis(OPT_FNAME, CHIPNAME, 1, log)
            # Analysis(OPT_FNAME, CHIPNAME, 2, log)
            # Analysis(OPT_FNAME, CHIPNAME, 3, log)


        ## Output file arrangement part
        name = "/".join(OPT_FNAME.split("/")[1:])
        print(name)
        pattern1 = "home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/data/"
        pattern2 = r"run\d{9}_\d{12}\.raw"
        pathname_tmp = re.sub(pattern1, '', name)
        pathname = re.sub(pattern2, '', pathname_tmp)
        print(pathname)

        pattern3 = r"/VCASB_\d{2,3}/run\d{9}_\d{12}\.raw" ## for old datasets, like 5_2_W24B5
        # pattern3 = r"/VCASB\d{2,3}/run\d{9}_\d{12}\.raw"
        pathname_v2 = re.sub(pattern3, '', pathname_tmp)
        print(pathname_v2)

        outputdir = pathlib.Path("/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/%s"%(pathname))
        outputdir.mkdir(parents=True,exist_ok=True)
        print(outputdir)

        outputfiles_final = glob.glob(f"/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/{CHIPNAME}_{Halfunit}_analysis_reg{region_number}.root")

        if not len(outputfiles_final) == 1:
            print("Why the final output files are more than 1. Please check it.")
            sys.exit(1)

        for file in outputfiles_final:
            os.system("mv %s %s/"%(file, outputdir))
        os.system(f"mv output.txt {outputdir}/")
        os.system("ls %s/"%(outputdir))

    outputfiles_common = glob.glob("/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/*.root")
    print(outputfiles_common)

    for file in outputfiles_common:
        os.system("mv %s /home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/%s/"%(file, pathname_v2))

    os.system("cp -r /home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/MaskCreator /home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/%s/"%(pathname_v2))
    os.system("ls /home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/output/%s/"%(pathname_v2))

    # 코드 끝나고 알림 보내기 
    webhook_url = "https://mattermost.web.cern.ch/hooks/ifkx4g9gupf4zcuz53bo98pqhr" 
    send_mattermost_alert(webhook_url, "run_first 코드 실행이 완료되었습니다!")


# 새로운 딕셔너리를 생성하는 함수
def extract_first_elements(original_dict):
    new_dict = {}
    for key, values in original_dict.items():
        # 값 리스트가 비어 있지 않다면 첫 번째 요소를 새로운 딕셔너리에 추가
        if values:  # 리스트가 비어 있지 않은지 확인
            new_dict[key] = values[0]
        else:
            # 옵션: 리스트가 비어 있을 경우 예외 처리 또는 기본값 설정
            new_dict[key] = None  # 또는 적절한 기본값 설정
    return new_dict

def check_highest_threshold(first_elements_dict, region_number, vcasb_value):
    highest_thresholds = first_elements_dict
    print(highest_thresholds)

    if region_number in highest_thresholds and vcasb_value == highest_thresholds[region_number]:
        print(f"this is the highest threshold in region {region_number}")
        return "y"
    else:
        print("this is not the highest threshold. masking with the existed file in the dir")
        return "n"


def create_mask(OPT_FNAME, CHIPNAME, Halfunit, SIDE, log, CHIP_TYPE):

    cmd = [
        "/home/jiyoung/AnalysisPrograms/corryvreckan/bin/corry",
        "-c", "configs/2024-05_PS/createmask.conf", 
        "-o", OPT_FNAME,
        "-o", f"MaskCreator.new_config_SUFFIX=_{CHIPNAME}_{Halfunit}",
        "-o", f"detectors_file=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{SIDE}.conf",
        "-o", f"detectors_file_updated=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_masked.conf",
        "-o", f"histogram_file={CHIPNAME}_{Halfunit}_maskcreation.root"
    ]

    print("------------------ Create Mask ------------------ ")
    print("Running command:", cmd)
    result = subprocess.run(cmd, stdout=log)
     
    if result.returncode != 0:
        print(f"Error creating mask: {result.stderr}")
    else:
        print("Mask creation successful.")


def pre_alignment(OPT_FNAME, CHIPNAME, Halfunit, log, CHIP_TYPE):

    cmd = [
        "/home/jiyoung/AnalysisPrograms/corryvreckan/bin/corry",
        "-c", "configs/2024-05_PS/prealign.conf", 
        "-o", OPT_FNAME,
        "-o", f"detectors_file=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_masked.conf",
        "-o", f"detectors_file_updated=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_prealigned.conf",
        "-o", f"histogram_file={CHIPNAME}_{Halfunit}_prealignment.root"
    ]

    print("------------------ Pre-alignment ------------------ ")
    print("Running command:", cmd)
    result = subprocess.run(cmd, stdout=log)

    # print("stdout:", result.stdout)
    # print("stderr:", result.stderr)

    if result.returncode != 0:
        print(f"Error prealignment: {result.stderr}")
    else:
        print("Prealignment process successful.")


def ALPIDE_alignment(OPT_FNAME, CHIPNAME, Halfunit, log, CHIP_TYPE):

    cmd = [
        "/home/jiyoung/AnalysisPrograms/corryvreckan/bin/corry",
        "-c", "configs/2024-05_PS/align.conf", 
        "-o", OPT_FNAME,
        "-g", "MOSS_reg0_3.role=passive",
        "-g", "MOSS_reg1_3.role=passive",
        "-g", "MOSS_reg2_3.role=passive",
        "-g", "MOSS_reg3_3.role=passive",
        "-o", f"detectors_file=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_prealigned.conf",
        "-o", f"detectors_file_updated=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_aligned_alpide.conf",
        "-o", f"histogram_file={CHIPNAME}_{Halfunit}_alignment_alpide.root"
    ]
   
    print("------------------ ALPIDE-alignment ------------------ ")
    print("Running command:", cmd)
    result = subprocess.run(cmd, stdout=log)

    if result.returncode != 0:
        print(f"Error prealignment: {result.stderr}")
    else:
        print("ALPIDE alignment process successful.")


def DUT_alignment(OPT_FNAME, CHIPNAME, Halfunit, role_index, log, CHIP_TYPE):

    role_config = ["passive", "passive", "passive", "passive"]
    role_config[role_index] = "dut"

    cmd = [
        "/home/jiyoung/AnalysisPrograms/corryvreckan/bin/corry",
        "-c", "configs/2024-05_PS/align.conf", 
        "-o", OPT_FNAME,
        "-g", f"MOSS_reg0_3.role={role_config[0]}",
        "-g", f"MOSS_reg1_3.role={role_config[1]}",
        "-g", f"MOSS_reg2_3.role={role_config[2]}",
        "-g", f"MOSS_reg3_3.role={role_config[3]}",
        "-o", f"detectors_file=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_aligned_alpide.conf",
        "-o", f"detectors_file_updated=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_aligned_reg{role_index}.conf",
        "-o", f"histogram_file={CHIPNAME}_{Halfunit}_alignment_reg{role_index}.root"
    ]

    print("------------------ DUT-alignment ------------------ ")
    print("Running command:", cmd)
    result = subprocess.run(cmd, stdout=log)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print(f"DUT Alignment for region {role_index} completed successfully.")


def Analysis(OPT_FNAME, CHIPNAME, Halfunit, role_index, log, CHIP_TYPE):

    role_config = ["auxiliary", "auxiliary", "auxiliary", "auxiliary"]
    role_config[role_index] = "dut"

    cmd = [
        "/home/jiyoung/AnalysisPrograms/corryvreckan/bin/corry",
        "-c", "configs/2024-05_PS/analyse.conf", 
        "-o", OPT_FNAME,
        "-g", f"MOSS_reg0_3.role={role_config[0]}",
        "-g", f"MOSS_reg1_3.role={role_config[1]}",
        "-g", f"MOSS_reg2_3.role={role_config[2]}",
        "-g", f"MOSS_reg3_3.role={role_config[3]}",
        "-o", f"detectors_file=/home/jiyoung/AnalysisPrograms/its-corryvreckan-tools/geometry/2024-09_PS_3REF-{CHIP_TYPE}-3REF_{CHIPNAME}_{Halfunit}_aligned_reg{role_index}.conf",
        "-o", f"histogram_file={CHIPNAME}_{Halfunit}_analysis_reg{role_index}.root"
    ]

    print("------------------ Analysis ------------------ ")
    print("Running command:", cmd)
    result = subprocess.run(cmd, stdout=log)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print(f"Analysis for region {role_index} completed successfully.")


if __name__ == "__main__":
    main(sys.argv)






