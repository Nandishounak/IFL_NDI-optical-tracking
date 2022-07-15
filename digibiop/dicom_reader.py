import os.path
import pathlib

import pydicom as dicom
from pydicom.data import get_testdata_file
from pydicom.filereader import dcmread
from pathlib import Path
path = pathlib.PureWindowsPath('E:\IFL\digibiop\\0001211180\DICOMDIR')
# p= get_testdata_file(path)
# path = get_testdata_file('DICOMDIR')

# import matplotlib.pyplot as plt
# filepath = get_testdata_files("E:\IFL\digibiop\0001211180\DICOM")
# print(filepath)
# os.path.join(("E:\IFL\digibiop\0001211180\DICOM"))
# dicom_dir = dicom.dcmread("E:\IFL\digibiop\0001211180\DICOM")
# print(dicom_dir)
# test_read = dicom.read_file("E:\IFL\digibiop\EE5D33F2", force=True)
# print(test_read[0x0018,0x1030])
#
# test_read = dicom.read_file("E:\IFL\digibiop\EE3AEA90", force=True)
# print(test_read[0x0018,0x1030])
#



ds = dcmread(path)
root_dir = Path(ds.filename).resolve().parent
print(f'Root directory: {root_dir}\n', 'path=', path)
import os
os.environ['PATH'] = 'E:\\Imfusion\\ImFusion Suite\\Suite;E:\\Imfusion\\ImFusion Suite\\Suite\\plugins;' + os.environ['PATH']
os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ';E:\\Imfusion\\ImFusion Suite\\Suite;'
# PYTHONUNBUFFERED = 1;PYTHONPATH="E:\Imfusion\ImFusion Suite\Suite"

import imfusion
imfusion.init()

