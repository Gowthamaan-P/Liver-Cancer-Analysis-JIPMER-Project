import dicom2numpy
import numpy2obj
import fileHandler
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount < 4:
	print("Invalid number of argument.")

option = sys.argv[1]
fname = str(sys.argv[2])
threshold = sys.argv[3]
foutput = str(sys.argv[4])
#npysaveoption = sys.argv[5]#not here yet (option to save npy)

tempNpy = dicom2numpy.main(fileHandler.dicomPath + slash + fname, fname)#not done
if argCount == 5:
	numpy2obj.main(tempNpy, threshold, foutput)
else:
	numpy2obj.main(tempNpy, threshold)