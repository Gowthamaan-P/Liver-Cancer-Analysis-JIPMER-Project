# Liver-Cancer-Analysis-JIPMER-Project
Development of 3D Visualization and Volumetry Analysis for Liver Tumour Diagnosis Using Artificial Intelligence

![image](https://user-images.githubusercontent.com/70436525/164887184-a946a030-853f-4e07-8aca-cbf730ee671d.png)


A python application which utilises marching cubes algorithm(skimage library) to generate 3D mesh from Dicom image stack of liver ct scan, which then can be output to .obj file(can be previewed using 3D viewer from microsoft store) and also finds the volume of liver and liver tumour.

## Requirements:
Python 3.7 or above

## Dependencies:
- Anaconda https://www.anaconda.com/distribution/ (or alternatively, each dependencies can be install separately)
    - Numpy https://www.numpy.org/
    - Scipy https://www.scipy.org/
    - Matplotlib https://pypi.org/project/matplotlib/
- Pydicom https://pydicom.github.io/
- GDCM http://gdcm.sourceforge.net/wiki/index.php/Main_Page (conda install -c conda-forge gdcm)
- Skit-image https://scikit-image.org/
- Sklearn https://scikit-learn.org/stable/
- NiBabel https://nipy.org/nibabel/

### Refs:
- https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/      14/06/19
- https://wiki.idoimaging.com/index.php?title=Sample_Data   seems like the have some dicoms and a bit of niftis we can playwith    17/06/19
- https://www.researchgate.net/post/What_is_the_easiest_way_to_batch_resize_DICOM_files to down sample dicoms, incase if they're too large  17/06/19
- https://stackoverflow.com/questions/55560243/resize-a-dicom-image-in-python      this one is for python. the one above is for mathlab, i didn't see
- https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python   export mesh to obj   17/06/19
