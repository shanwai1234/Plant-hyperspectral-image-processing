# Plant hyperspectral image processing in python-opencv for Lemnatec system
=======
This is the python-opencv code used for generating the average intensity of plant area under wavelength ranging from 546-1,700 nm.
opencv_hyperspectral.py is the original code.

The demo command to run this code is "python opencv_hyperspectral.py test.txt wavelength_foldid.txt"

wavelength_foldid.txt is the file showing images in the folder corresponding to actual wavelength, and they are all same in UNL corn phenomap project.

HYP_SV_90_far is the folder including images of one single plant in one day ranging from 0_0_0.png to 244_0_0.png, first image just tested from RGB channel for one image, and the second shows the information for each capturing time, but both of them are not used for calculating the average intensity.

test.txt is the demo file to show the result of wavelength and its corresponding intensity for each plant.

binary.jpg is the binary image printed out to see the binarization, but this is just a check and not necessary for the code.

stem.jpg is the binary image with only stem printer out to see the effect, while also a check file and not necessary for the code.

final.jpg is the merged binary image for whole plant without the stem part, and also is a check file.
