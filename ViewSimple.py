from __future__ import print_function
import sys
import os
from itk import imread
from SimpleITK import ImageSeriesReader, WriteImage
from ipywidgets.embed import embed_minimal_html
from itkwidgets import view
import webbrowser
import numpy as np
from nrrd import read 
from nibabel import Nifti1Image, save, load

# Directory names
dirName = "F:\\Liver Project\\Patient 1\\Segmented Liver\\"
maskDir = "F:\\Liver Project\\Patient 1\\Segmented Tumour\\"
outputName = input("Enter the name of the output Liver file: ")
tumourName = input("Enter the name of the output Tumour file: ")

# Reading the series of DICOM for Liver
print("Reading Dicom directory:", dirName)
reader = ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(dirName)
reader.SetFileNames(dicom_names)
image = reader.Execute()
size = image.GetSize()
print("Writing image: ", outputName+".nrrd")
WriteImage(image, outputName+".nrrd")

# Reading the series of DICOM for Tumour
print("Reading Dicom directory:", maskDir)
reader = ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(maskDir)
reader.SetFileNames(dicom_names)
image = reader.Execute()
size = image.GetSize()
print("Writing image: ", tumourName+".nrrd")
WriteImage(image, tumourName+".nrrd")

# Viewing Liver
image = imread(outputName+".nrrd")
views = view(image)
embed_minimal_html(outputName+".html",views = [views],title = "Export")
webbrowser.open_new_tab(outputName+".html")

# Viewing Tumour
seg = imread(tumourName+".nrrd")
views = view(seg)
embed_minimal_html(tumourName+".html",views = [views],title = "Export")
webbrowser.open_new_tab(tumourName+".html")

# Tumour Segmented Liver
seg.CopyInformation(image)
views = view(image,seg)
view(image,seg)
embed_minimal_html(tumourName+" segmented "+outputName+".html",views = [views],title = "Export")
webbrowser.open_new_tab(tumourName+" segmented "+outputName+".html")

# nii file generation
# load nrrd 
_nrrd = read(outputName + ".nrrd")
data = _nrrd[0]
header = _nrrd[1]
# save nifti
img = Nifti1Image(data, np.eye(4))
save(img, outputName + '.nii')
# for tumour nrrd
_nrrd = read(tumourName + ".nrrd")
data = _nrrd[0]
header = _nrrd[1]
# save nifti
img = Nifti1Image(data, np.eye(4))
save(img, tumourName + '.nii')

# Liver volume calculation
img_np = np.array(image) #convert to numpy array
binarry = np.where(img_np>0,1,0)  #binary array - one where liver is present, zero where it is not
space = image.GetSpacing() #starting from the origin location of the model
voxel = np.prod(space)     #one voxel unit volume analogous to pixel in 2d
vol = voxel*np.sum(binarry) #total volume = no. of voxels * volume unit voxel
print(outputName+" volume: " + str(vol/1000) + " cc") #total volume of liver in cc

# Total Tumour volume calculation
img_np = np.array(seg) 
binarry = np.where(img_np>0,1,0)  
space = image.GetSpacing() 
voxel = np.prod(space)     
vol = voxel*np.sum(binarry) 
print("Total "+tumourName+" volume: " + str(vol/1000) + " cc") 

# Aggressive tumour volume calculation
img_seg_nii = load(tumourName+".nii")
img_seg_np = np.array(seg)
slope = img_seg_nii.dataobj.slope
inter = img_seg_nii.dataobj.inter
hu = np.where(img_seg_np > 0, (img_seg_np*slope + inter),0)
agg_tumour = np.where(hu > 90,1,0)
agg_vol = np.sum(agg_tumour)*voxel
print("Aggressive "+tumourName+" volume: " + str(agg_vol/1000) + " cc")

# Moderately Agg volume calculation
mod_tumour = np.where(hu < 90,1,0)
mod_tumour_1 = np.where(hu > 45,1,0)
mod_tumour = mod_tumour * mod_tumour_1
mod_vol = np.sum(mod_tumour)*voxel
print("Moderately Aggressive "+tumourName+" volume: " + str(mod_vol/1000) + " cc")

# Less Agg volume calculation
less_tumour = np.where(hu < 45,1,0)
less_tumour_1 = np.where(hu > 0,1,0)
less_tumour = less_tumour * less_tumour_1
less_agg = np.sum(less_tumour)*voxel
print("Less Aggressive "+tumourName+" volume: " + str(less_agg/1000) + " cc")

exit(0)
