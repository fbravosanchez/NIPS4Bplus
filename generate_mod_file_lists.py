# -*- coding: utf-8 -*-
"""
Created by Francisco Bravo Sanchez July 2021

Generates NIPS4Bplus test and train datasets to run on the modified SincNet
code

Generates train and test sets for three selections of classes: "All Classes", 
"Bird Classes" and "Bird Species"

NIPS4Bplus annotations:
https://doi.org/10.6084/m9.figshare.6798548

NIPS4B species list:
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_LABELS.tar
Choose: nips4b_birdchallenge_espece_list.csv

Instructions
https://github.com/fbravosanchez/NIPS4Bplus#readme
"""


import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
import sys


def export_csv(file, name):
    file.to_csv(os.path.join(output_path, '') + name +'.csv',index=False, header=True, encoding='utf-8')



#path to NIPS4Bplus csv annotation files
annotations_path=sys.argv[1]
#path to NIPS4B species list
sps_list_file=sys.argv[2]
#output path for csv list files
output_path=sys.argv[3]


if not os.path.exists(output_path):
    os.makedirs(output_path)

#collect csv label file list
lbl_files = pd.DataFrame(glob.glob(os.path.join(annotations_path, '') + '*.csv'))
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
    except pd.errors.EmptyDataError:
        tags = False

    #for each valid csv file process tags
    if tags:
        for l, m in k.iterrows():
            file_out = str(j['wav'])+'.wav'
            try:
                type_out = sps_list.loc[sps_list['class name'] ==
                                        m[2]].type.values[0]
                scient_out = sps_list.loc[sps_list['class name'] ==
                                          m[2]].Scientific_name.values[0]
            except:
                type_out = ''
                scient_out = ''
            dict_out = dict(zip(['file', 'type', 'class_name', 'species', 'start', 'length'],
                                [file_out, type_out, m[2], scient_out, m[0],m[1]]))
            file_list.append(dict_out)

file_list = pd.DataFrame(file_list)


#%% all classes
all_classes = file_list[file_list['type'] != '']

#Generate label dictionary files for all classes
all_classes_dict = pd.DataFrame(all_classes['class_name'].unique())
all_classes_dict.reset_index(drop=False, inplace=True)
all_classes_dict.columns = ['label', 'class_name']
all_classes = pd.merge(all_classes, all_classes_dict, how='left', on=['class_name'])


#Randomly split into train and test
train_files, test_files = train_test_split(all_classes, stratify=all_classes['label'], test_size=0.25)

# export file lists
export_csv(train_files, 'mod_all_classes_train_files')
export_csv(test_files, 'mod_all_classes_test_files')


#%% bird classes

bird_classes = file_list[file_list['type'] == 'bird']

#Generate label dictionary files for bird classes
bird_classes_dict = pd.DataFrame(bird_classes['class_name'].unique())
bird_classes_dict.reset_index(drop=False, inplace=True)
bird_classes_dict.columns = ['label', 'class_name']
bird_classes = pd.merge(bird_classes, bird_classes_dict, how='left', on=['class_name'])

#Randomly split into train and test
train_files, test_files = train_test_split(bird_classes, stratify=bird_classes['label'], test_size=0.25)

# export file lists
export_csv(train_files, 'mod_bird_classes_train_files')
export_csv(test_files, 'mod_bird_classes_test_files')


#%% bird species

bird_species = file_list[file_list['type'] == 'bird']

#Generate label dictionary files for bird classes
bird_sps_dict = pd.DataFrame(bird_species['species'].unique())
bird_sps_dict.reset_index(drop=False, inplace=True)
bird_sps_dict.columns = ['label', 'species']

bird_species = pd.merge(bird_species, bird_sps_dict, how='left', on=['species'])

#Randomly split into train and test
train_files, test_files = train_test_split(bird_species, stratify=bird_species['label'], test_size=0.25)

# export file lists
export_csv(train_files, 'mod_bird_sps_train_files')
export_csv(test_files, 'mod_bird_sps_test_files')

