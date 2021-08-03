# -*- coding: utf-8 -*-

"""
Created by Francisco Bravo Sanchez July 2021
This script reads the csv annotations from NIPS4Bplus and the species list from
NIPS4B to generate list of train and test files and dictionary label files

The dictionary files list random train and test sets for three selections of
classes: "All Classes", "Bird Classes" and "Bird Species"

It generates two separate test and train file sets. One for "All Classes" and a 
different one "birds" for both "Bird Classes" and "Bird Species"

NIPS4Bplus annotations:
https://doi.org/10.6084/m9.figshare.6798548

NIPS4B species list:
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_LABELS.tar
Choose: nips4b_birdchallenge_espece_list.csv

Instructions
https://github.com/fbravosanchez/NIPS4Bplus#readme
"""


import sys
import os
import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as tr_te_split


def export_scp(file, name):
    file.to_csv(os.path.join(output_path, '') + name +'.scp',index=False, header=False, encoding='utf-8')

def export_npy(file, name):
    np.save(os.path.join(output_path, '') + name + '.npy', file)


#path to NIPS4Bplus csv annotation files
csv_path = sys.argv[1]
#path to NIPS4B species list
sps_list_file = sys.argv[2]
#path to cut files generated in cut_nips4bplus_files
# cut_files_path = sys.argv[3]
#output path for dictionary files
output_path = sys.argv[3]


if not os.path.exists(output_path):
    os.makedirs(output_path )


#collect csv label file list
lbl_files = pd.DataFrame(glob.glob(os.path.join(csv_path, '') + '*.csv'))
lbl_files.columns = ['csv']
lbl_files['wav'] = 'nips4b_birds_trainfile' + lbl_files['csv'].str[-7:-4]

#read species list
sps_list = pd.read_csv(sps_list_file)


file_list = []

#process by csv file
for i, j in lbl_files.iterrows():

    #skip empty files
    try:
        k = pd.read_csv(j['csv'], header=None)
        tags = True
    except pd.io.common.EmptyDataError:
        tags = False

    #for each valid csv file process tags
    if tags:
        for l, m in k.iterrows():
            #exclude files less than 10ms
            if m[1] > 0.01:
                file_out = str(j['wav'])+'_'+str(l)+'.wav'
                try:
                    type_out = sps_list.loc[sps_list['class name'] ==
                                            m[2]].type.values[0]
                    scient_out = (sps_list.loc[sps_list['class name'] ==
                                               m[2]].Scientific_name.values[0])
                except:
                    type_out = ''
                    scient_out = ''
                dict_out = dict(zip(['File', 'Type', 'Class', 'Scientific'],
                                    [file_out, type_out, m[2], scient_out]))
                file_list.append(dict_out)

file_list = pd.DataFrame(file_list)

#%% process all classes
file_list_all_classes = file_list[file_list['Type'] != '']

#Randomly split into train and test
tr_files, ts_files = tr_te_split(file_list_all_classes['File'], 
                                 stratify=file_list_all_classes['Class'], 
                                 test_size=0.25)

# save train and test file lists
export_scp(ts_files, 'all_classes_test_files')
export_scp(tr_files, 'all_classes_train_files')

#Generate label dictionary files for All Classes
unique_all_class = pd.DataFrame(file_list_all_classes['Class'].unique())
unique_all_class.reset_index(drop=False, inplace=True)
unique_all_class.columns = ['Value', 'Class']

merge_class = pd.merge(file_list_all_classes, unique_all_class, how='left', on=['Class'])
class_dict = dict(zip(merge_class.File, merge_class.Value))

export_npy(class_dict, 'all_classes_labels')


#%% process bird files
#Select only bird type files
file_list_birds = file_list[file_list['Type'] == 'bird']

#Repeat a random split into train and test including only birds
tr_files, ts_files = tr_te_split(file_list_birds['File'], 
                                 stratify=file_list_birds['Class'], 
                                 test_size=0.25)

# save train and test file lists
export_scp(ts_files, 'bird_test_files')
export_scp(tr_files, 'bird_train_files')

#%%generate label dictionary files for bird classes
unique_bird_class = pd.DataFrame(file_list_birds['Class'].unique())
unique_bird_class.reset_index(drop=False, inplace=True)
unique_bird_class.columns = ['Value', 'Class']

merge_class = pd.merge(file_list_birds, unique_bird_class, how='left', on=['Class'])
class_dict = dict(zip(merge_class.File, merge_class.Value))

export_npy(class_dict, 'bird_classes_labels')

#%%generate label dictionary files for bird species
unique_bird_sps = pd.DataFrame(file_list_birds['Scientific'].unique())
unique_bird_sps.reset_index(drop=False, inplace=True)
unique_bird_sps.columns = ['Value', 'Scientific']

merge_scient = pd.merge(file_list_birds, unique_bird_sps, how='left', on=['Scientific'])
scient_dict = dict(zip(merge_scient.File, merge_scient.Value))

export_npy(scient_dict, 'bird_species_labels')
