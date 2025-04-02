
[ALPIDE_0]
type = "ALPIDE"
position = 0mm,0mm,0mm
number_of_pixels = 1024,512
pixel_pitch = 29.24um, 26.88um
spatial_resolution = 4.2um, 4.0um
time_resolution = 2us
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,0deg
orientation_mode = xyz

[ALPIDE_1]
type = "ALPIDE"
position = 0mm,0mm,25mm
number_of_pixels = 1024,512
pixel_pitch = 29.24um, 26.88um
spatial_resolution = 4.2um, 4.0um
time_resolution = 2us
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,0deg
orientation_mode = xyz

[ALPIDE_2]
type = "ALPIDE"
position = 0mm,0mm,50mm
number_of_pixels = 1024,512
pixel_pitch = 29.24um, 26.88um
spatial_resolution = 4.2um, 4.0um
time_resolution = 2us
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,0deg
orientation_mode = xyz
role = "reference"

### MOSS ###

[MOSS_reg0_3]
type = "MOSS"
position = 10mm,0mm,82mm
number_of_pixels = 320,320
pixel_pitch = 18um, 18um
spatial_resolution = 5.2um, 5.2um  # let's start from the binary resolution of the pixel
time_resolution = 10s
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,180deg
orientation_mode = xyz
role = "auxiliary"
roi = [[40,0],[40,200],[320,200],[320,0]]

[MOSS_reg1_3]
type = "MOSS"
position = 4mm,0mm,82mm
number_of_pixels = 320,320
pixel_pitch = 18um, 18um
spatial_resolution = 5.2um, 5.2um  # let's start from the binary resolution of the pixel
time_resolution = 10s
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,180deg
orientation_mode = xyz
role = "auxiliary"
roi = [[0,0],[0,200],[320,200],[320,0]]

[MOSS_reg2_3]
type = "MOSS"
position = -2mm,0mm,82mm
number_of_pixels = 320,320
pixel_pitch = 18um, 18um
spatial_resolution = 5.2um, 5.2um  # let's start from the binary resolution of the pixel
time_resolution = 10s
material_budget = 0.0005 
coordinates = "cartesian"
orientation = 0deg,0deg,180deg
orientation_mode = xyz
role = "auxiliary"
roi = [[0,0],[0,200],[320,200],[320,0]]

[MOSS_reg3_3]
type = "MOSS"
position = -8mm,0mm,82mm
number_of_pixels = 320,320
pixel_pitch = 18um, 18um
spatial_resolution = 5.2um, 5.2um  # let's start from the binary resolution of the pixel
time_resolution = 10s
material_budget =  0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,180deg
orientation_mode = xyz
role = "auxiliary"
roi = [[0,0],[0,200],[280,200],[280,0]]
######

[ALPIDE_4]
type = "ALPIDE"
position = 0mm,0mm,125mm
number_of_pixels = 1024,512
pixel_pitch = 29.24um,26.88um
spatial_resolution = 4.2um, 4.0um
time_resolution = 2us
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,0deg
orientation_mode = xyz

[ALPIDE_5]
type = "ALPIDE"
position = 0mm,0mm,150mm
number_of_pixels = 1024,512
pixel_pitch = 29.24um, 26.88um
spatial_resolution = 4.2um, 4.0um
time_resolution = 2us
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,0deg
orientation_mode = xyz

[ALPIDE_6]
type = "ALPIDE"
position = 0mm,0mm,175mm
number_of_pixels = 1024,512
pixel_pitch = 29.24um, 26.88um
spatial_resolution = 4.2um, 4.0um
time_resolution = 2us
material_budget = 0.0005
coordinates = "cartesian"
orientation = 0deg,0deg,0deg
orientation_mode = xyz
