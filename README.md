# NDI Polaris Vicra optical sensor to Imfusion Suite Transformation matrix calculator
This script generates the transformation matrix from NDI Polaris Vicra to Imfusion Suite; the calibration has been done on a wire phantom, taking 8 landmark points.
The Tranformation matrix offset from tip of the tool to the tracking markers are given.![stylus_with_coordinates](https://user-images.githubusercontent.com/89601329/182632877-0b175ddf-9e44-43c0-bf72-4878236a22dd.jpg)


**Assumptions**-
1. The wire phantom, the body phantom, the optical tracker is kept fixed during the calibration procedure.
2. The 8 landmark points, also termed as stl points in the scipt are stored in /home/nandishounak/Documents/IFL/ImFusionMhaExporter/stl_landmarks/ as .txt files, separately and as a combined so that we can calculate the matrix transform later. The names of the .txt files should be done in a way so that it stays sorted by names, for example, stl_01.txt, stl_02.txt, etc.
3. The stylus matrix offset transform from the tip to the marker head is known and stored as a .txt in /home/nandishounak/Documents/IFL/ImFusionMhaExporter/.
While recording the tracking stream data of different landmark points on the Imfusion Suite, rename the .imf files in a sequential manner so that it says sorted by name, for e.g. l01.imf, l07.imf, l11.imf.
4. The triangular marker data placed on the xyphoid process of the  body phantom is stored in 'average_pts_folder_body_phantom' folder.

**Steps of Implementation**- 
1. The coordinates of the landmark points from the wire phantom were noted with the help of ImFusion Suite.
2. 8 landmark points from the phantom were considered- 1, 2, 4, 5, 7, 8, 10 and 11.
3. Next the average pose of the pointer(NDI 4-marker probe) at these 8 points were calculated with the help of the script from the ImFusion Suite interfaced with NDI Polaris Vicra position sensor.
                            
![image](https://user-images.githubusercontent.com/89601329/184925948-4310f898-3e5d-412a-b331-18cb8b8e4469.png).

4. After the transformation matrix was calculated from the 8 points using Least square solutions, the matrix was then added to the ImFusion Suite --> apply transformations.
5. After applying the transformations, the live tracking position of the pointer is registered with the phantom stl, and it points to the respective data points, as done in the real world.
![image](https://user-images.githubusercontent.com/89601329/184932987-5b089cfb-2311-45ce-921a-de16aca7c87d.png)

