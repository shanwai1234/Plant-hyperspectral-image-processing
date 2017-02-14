# Plant hyperspectral image processing in python-opencv for Lemnatec system
=======
This is the python-opencv code used for generating the average intensity of plant area under wavelength ranging from 546-1,700 nm.
opencv_hyperspectral.py is the original code.
wavelength_foldid.csv is the file showing images in the folder corresponding to actual wavelength, and they are all same in UNL corn phenomap project.
HYP_SV_90_far is the folder including images of one single plant in one day ranging from 0_0_0.png to 244_0_0.png, first image just tested from RGB channel for one image, and the second shows the information for each capturing time, but both of them are not used for calculating the average intensity.
test.csv is the demo file to show the result of wavelength and its corresponding intensity for each plant. 
