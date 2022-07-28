import os
import csv
path=os.path.dirname("/mnt/projects/DeepProstateDB/Data/14/0001147395(multiple_times_of_scan)/README.txt") #just for testing
print(path)
print(os.path.basename(path))



my_list = os.listdir("/mnt/projects/DeepProstateDB/Data/15/")
print(my_list)
with open('/mnt/HDD1/shounak/patientids_15.csv', 'w') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(my_list)