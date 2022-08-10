# NDI Polaris Vicra optical sensor to Imfusion Suite Transformation matrix calculator
This script generates the transformation matrix from NDI Polaris Vicra to Imfusion Suite; the calibration has been done in a wire phantom, taking 8 landmark points.
The Tranformation matrix offset from tip of the tool to the tracking markers are given.![stylus_with_coordinates](https://user-images.githubusercontent.com/89601329/182632877-0b175ddf-9e44-43c0-bf72-4878236a22dd.jpg)
**Assumptions**-
1. The wire phantom, the body phantom, the optical tracker is kept fixed during the calibration procedure.
2. The 8 landmark points, also termed as stl points in the scipt are stored in /home/nandishounak/Documents/IFL/ImFusionMhaExporter/stl_landmarks/ as .txt files, separately and as a combined so that we can calculate the matrix transform later. The names of the .txt files should be done in a way so that it says sorted by names, for example, stl_01.txt, stl_02.txt, etc.
3. The stylus matrix offset transform from the tip to the marker head is known and stored as a .txt in /home/nandishounak/Documents/IFL/ImFusionMhaExporter/.
While recording the tracking stream data of different landmark points on the Imfusion Suite, rename the .imf files in a sequential manner so that it says sorted by name, for e.g. l01.imf, l07.imf, l11.imf.
