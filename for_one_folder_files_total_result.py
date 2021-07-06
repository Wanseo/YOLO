import os
import pandas as pd
import xml.etree.ElementTree as ET
from collections import Counter
from openpyxl import Workbook, load_workbook
import csv

# init
PIXEL= 4
TEXT_FILE = 'folders'

list_class = []
list_max = []
list_min = []
total_size = []
scaled_size= []
result = []
count = 0

cwd = '/'
dirname = 'Users/jowanseo/Desktop/{}'.format('01.cm_chn_d09_5126_labels_od_v1.0_20210615')
files = os.listdir('/Users/jowanseo/Desktop/{}'.format('01.cm_chn_d09_5126_labels_od_v1.0_20210615'))

    #  one folder, all files
for idx in range(len(files)):
        # only xml files
    if files[idx].endswith(".xml"):
        files[idx] = os.path.join(cwd, dirname, files[idx])
        doc = ET.parse(files[idx])
        root = doc.getroot()

        size_max = root.findall("object/bndbox/ymax")
        size_min = root.findall("object/bndbox/ymin")
        name_tag = root.findall("object/name")

        count+=1

        for i in name_tag:
            list_class.append(i.text)

        for i in size_max:
            list_max.append(float(i.text))

        for i in size_min:
            list_min.append(float(i.text))

total_size=[list_max[i] - list_min[i] for i in range(len(list_class))]
scaled_size = [int((total_size[i] - 1) / PIXEL) for i in range(len(list_class))]

# of class
num_class = Counter(list_class)
ob_name = []
ob_count = []

for key, val in dict(num_class).items():
    ob_name.append(key)
    ob_count.append(val)

cname = ob_name
rname = ['# of objects']
result_df = pd.DataFrame([ob_count], index=rname, columns=cname)

td = {
    'class': list_class,
    'pix_class': scaled_size
}

result = []
pdf_ = pd.DataFrame(td)

for i in ob_name:
    is_ = pdf_['class'] == i
    df_n = pdf_[is_]
    val_li = df_n['pix_class'].values
    c = Counter(val_li)
    result.append(c)

array = [[0 for col in range(len(ob_name))] for row in range(181)]

for j in range(len(ob_name)):
    for key, val in dict(result[j]).items():
        array[key][j] += val

cat_index = []
k = 1

for i in range(1, 182):
    posi_int = k + 3
    cat_index.append('{}~{}'.format(k, posi_int))
    k = posi_int + 1

array_df = pd.DataFrame(array, columns=ob_name, index=cat_index)

# Final result
result_df = pd.concat([result_df, array_df])

f = open('/Users/jowanseo/Desktop/xml_results/{}.csv'.format('01.cm_chn_d09_5126_labels_od_v1.0_20210615'), 'w', newline='')
wr = csv.writer(f)
wr.writerow(['file name {}'.format('01.cm_chn_d09_5126_labels_od_v1.0_20210615')])
wr.writerow(['# of image {}'.format(count)])
wr.writerow(['A3''step size {}'.format(PIXEL)])
f.close()

with open('/Users/jowanseo/Desktop/xml_results/{}.csv'.format('01.cm_chn_d09_5126_labels_od_v1.0_20210615'), 'a') as f:
    result_df.to_csv(f, header=True)