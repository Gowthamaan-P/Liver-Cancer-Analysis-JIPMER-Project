#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
import matplotlib.pyplot as plt
import pydicom
import scipy.ndimage
from skimage import measure 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from os import listdir
from plotly.offline import iplot
from plotly.tools import FigureFactory as FF


# In[18]:


LiverPath = "F:\\Liver Project\\Patient 1\\Segmented Liver\\"
TumourPath = "F:\\Liver Project\\Patient 1\\Segmented Tumour\\"


# In[19]:


def LoadScans(Path):
    slices = [pydicom.dcmread(Path + "\\" + file) for file in listdir(Path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    return slices


# In[20]:


LiverScans = LoadScans(LiverPath)
TumourScans = LoadScans(TumourPath)


# In[21]:


def FindVolume(hu_scans,part):
    Volume=0;
    if part == "Liver":
        for i in range(len(hu_scans)):
            for j in range (len(hu_scans[i])):
                Area = 0.1 * LiverScans[i].PixelSpacing[0] * 0.1 * LiverScans[i].PixelSpacing[1] * np.count_nonzero(hu_scans[i,j])
                Volume += 0.1 * LiverScans[i].SliceThickness * Area
        return Volume
    else:
        for i in range(len(hu_scans)):
            for j in range (len(hu_scans[i])):
                Area = 0.1 * TumourScans[i].PixelSpacing[0] * 0.1 * TumourScans[i].PixelSpacing[1] * np.count_nonzero(hu_scans[i,j])
                Volume += 0.1 * TumourScans[i].SliceThickness * Area
        return Volume


# In[22]:


def FindHUValues(slices):
    images = np.stack([file.pixel_array for file in slices])
    images = images.astype(np.int16)
#     images[images == -2000] = 0
    for n in range(len(slices)):
        intercept = slices[n].RescaleIntercept
        slope = slices[n].RescaleSlope
        if slope != 1:
            images[n] = slope * images[n].astype(np.float64)
            images[n] = images[n].astype(np.int16)
        images[n] += np.int16(intercept)
    return np.array(images, dtype=np.int16)


# In[23]:


LiverHU = FindHUValues(LiverScans)
TumourHU = FindHUValues(TumourScans)

TumourHU = np.where(TumourHU > 150, 0, TumourHU)#Omitting all values greaer than 256 because of input error
MildHU = np.where(TumourHU <= 46, 0, TumourHU)
ModerateHUDummy = np.where(TumourHU <= 91, 0, TumourHU)
ModerateHU = np.where(ModerateHUDummy >= 46, 0, ModerateHUDummy)
AggressiveHU = np.where(TumourHU >= 91, 0, TumourHU)


# In[25]:


LiverVolume = FindVolume(LiverHU,"Liver")
TumourVolume = FindVolume(TumourHU,"Tumour")
MildVolume = FindVolume(MildHU,"Tumour")
ModerateVolume = FindVolume(ModerateHU,"Tumour")
AggressiveVolume = FindVolume(AggressiveHU,"Tumour")


print("Liver Volume:", LiverVolume)
print("Tumour Volume:", TumourVolume)
print("Moderate Tumour Volume:", MildVolume)
print("Aggressive Tumour Volume:", AggressiveVolume)


# In[26]:


def Plot3D(LiverHUResampled, MildHUResampled, AggressiveHUResampled, threshold=30):
    
    verts, faces,_,_ = measure.marching_cubes_lewiner(LiverHUResampled, threshold)
    x,y,z = zip(*verts)
    colormap=['rgba(255, 0, 0, 0.5)','rgba(255, 0, 0, 0.5)']
    FigLiver = FF.create_trisurf(x=x, y=y, z=z, 
                            plot_edges=False,
                            colormap=colormap,
                            simplices=faces,
                            backgroundcolor='rgb(64, 64, 64)',
                            title="3D Visualization of Liver")
    
    verts, faces,_,_ = measure.marching_cubes_lewiner(MildHUResampled, threshold)
    x,y,z = zip(*verts)
    colormap=['rgba(0, 0, 255, 0.5)','rgba(0, 0, 255, 0.5)']
    FigModerate = FF.create_trisurf(x=x, y=y, z=z, 
                            plot_edges=False,
                            colormap=colormap,
                            simplices=faces,
                            backgroundcolor='rgb(64, 64, 64)',
                            title="3D Visualization of Mild Tumour")
    
    verts, faces,_,_ = measure.marching_cubes_lewiner(AggressiveHUResampled, threshold)
    x,y,z = zip(*verts)
    colormap=['rgba(0, 0, 0, 0.5)','rgba(0, 0, 0, 0.5)']
    FigAggressive = FF.create_trisurf(x=x, y=y, z=z, 
                            plot_edges=False,
                            colormap=colormap,
                            simplices=faces,
                            backgroundcolor='rgb(64, 64, 64)',
                            title="3D Visualization of Aggressive Tumour")
    FigLiver['data'][0].update(opacity=0.5)
    FigModerate['data'][0].update(opacity=0.5)
    FigAggressive['data'][0].update(opacity=0.5)

    iplot(FigLiver) 
    iplot(FigModerate)    
    iplot(FigAggressive)    


# In[27]:


def Resample(image, scan, new_spacing=[1,1,1]):
    spacing = np.array([scan[0].SliceThickness] + list(scan[0].PixelSpacing), dtype=np.float32)
    resize_factor = spacing / new_spacing
    new_shape = np.round(image.shape * resize_factor)
    rounded_resize_factor = new_shape / image.shape
    rounded_new_spacing = spacing / rounded_resize_factor
    image = scipy.ndimage.interpolation.zoom(image, rounded_resize_factor, mode='nearest')
    return image, rounded_new_spacing


# In[28]:


LiverHUResampled, _= Resample(LiverHU, LiverScans)
ModerateHUResampled, _= Resample(ModerateHU, TumourScans)
AggressiveHUResampled, _= Resample(AggressiveHU, TumourScans)

LiverHUResampledTranspose = LiverHUResampled.transpose(2,1,0)
ModerateHUResampledTranspose = ModerateHUResampled.transpose(2,1,0)
AggressiveHUResampledTranspose = AggressiveHUResampled.transpose(2,1,0)


# In[29]:


Plot3D(LiverHUResampledTranspose, MildHUResampledTranspose, AggressiveHUResampledTranspose)


# In[ ]:




