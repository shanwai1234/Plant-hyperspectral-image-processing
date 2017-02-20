import numpy as np
import cv2 
from matplotlib import pyplot as plt
import os
import sys

# create a funtion to binary segmented photos
def binary(pic):
	final = []
	myl = np.shape(pic)[0]
	myw = np.shape(pic)[1]
	for i in pic:
		n = []
		for j in i:
			# only for each pixel that greater than 0.25 were converted to whole white pixel, while pixel value less than that was converted to black
			if j > 0.25:
				t = 255
			else:
				t = 0
			n.append(t)
		final.append(n)
	final = np.array(final)	
	return final

# create a funtion to remove stem
def rmstem(pic1,pic2):
	mypic = []
	myl = np.shape(pic1)[0]
	myw = np.shape(pic1)[1]
	for i in range(myl):
		n = []
		for j in range(myw):
			if pic1[i,j] == 0 or pic2[i,j] == 0:
				n.append(0)
			else:
				ratio = pic1[i,j]/pic2[i,j]
				if ratio > 1.2:
					n.append(255)
				else:
					n.append(0)
		mypic.append(n)
	mypic = np.array(mypic)
	return mypic

# create a function to merge first binaried image and stem removed image together
def merge(pic1,pic2):
	final = []
	myl = np.shape(pic1)[0]
	myw = np.shape(pic1)[1]
	for i in range(myl):
		n = []
		for j in range(myw):
			diff = pic1[i,j]-pic2[i,j]
			if diff <= 0:
				n.append(0)
			else:
				n.append(255)
		final.append(n)
	final = np.array(final)
	return final

# out file is the output of average intensity in plant area in each photo of one folder
out = open(sys.argv[1],'w')
# sh is the reference file showing which file corresponds to which wavelength
sh = open(sys.argv[2],'r')
sh.readline()
kdict = {}
# build a library to include file~wavelength information
for line in sh:
	new = line.strip().split('\t')
	kdict[new[4]] = new[0]

# in every folder, the images of 35_0_0.png and 45_0_0.png should be used firstly in order to subtract the plant area
m705 = cv2.imread("HYP_SV_90_far/35_0_0.png")
m750 = cv2.imread("HYP_SV_90_far/45_0_0.png")

# these files are used to remove stem area in one plant
m1056 = cv2.imread("HYP_SV_90_far/108_0_0.png")
m1151 = cv2.imread("HYP_SV_90_far/128_0_0.png")

# converting plant images from RGB to GRAY channel
tm705 = cv2.cvtColor(m705,cv2.COLOR_BGR2GRAY)
tm750 = cv2.cvtColor(m750,cv2.COLOR_BGR2GRAY)

tm1056 = cv2.cvtColor(m1056,cv2.COLOR_BGR2GRAY)
tm1151 = cv2.cvtColor(m1151,cv2.COLOR_BGR2GRAY)

tm1056 = tm1056.astype(np.float)
tm1151 = tm1151.astype(np.float)

rmg = rmstem(tm1056,tm1151)

# use NDVI to identify the outline of plant, which is (750nm-705nm)/(750nm-705nm)
k = np.subtract(tm750.astype(np.float),tm705.astype(np.float))
j = np.add(tm750.astype(np.float),tm705.astype(np.float))

img = cv2.divide(k,j,scale=1)
# image in NDVI index is going to perform binarization 
mmg = binary(img)

tmg = merge(mmg,rmg)
# This is going to print out the image and help to check if the binarization process works well, but can skip that in bundle of processing.		
cv2.imwrite('binary.jpg',mmg)
cv2.imwrite('stem.jpg',rmg)
cv2.imwrite('final.jpg',tmg)

tmg = tmg/255.0
myfold = os.listdir('HYP_SV_90_far')
mdict = {}
for i in myfold:
	# first two images are not useful and just skip them
	if i == '0_0_0.png':continue
	if i == '1_0_0.png':continue
	# info.txt is not an image file
	if i == 'info.txt':continue
	name = i.replace('_0_0.png','')
	t = cv2.imread("HYP_SV_90_far/{0}".format(i))
	t = t.astype(np.float)
	t1 = t[:,:,0]
	t3 = t1/255.0
	# multiply each files in the folder with the binarized image. For each pixel, dividing 255 to make each pixel in 0~1 
	t2 = np.multiply(t1/255.0,tmg)
	total = 0
	plant = tmg.sum()
	# l*m is the total number of pixels inside one image
	for n in t2:
		for m in n:
			total += m
	avg = total/plant
	mdict[name] = avg*255

# print out the average intensity of each file in each image folder
for i in range(2,245):
	i = str(i)
	out.write(kdict[i]+','+str(mdict[i])+'\n')
