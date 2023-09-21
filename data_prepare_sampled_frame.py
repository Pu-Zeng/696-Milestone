import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import mido
import string
import numpy as np
from utilis import get_pianoroll_data
import pickle
label_data = {'genre':'msd-MAGD-genreAssignment.cls', 'style':'msd-MASD-styleAssignment.cls', 'genre_more':'msd-topMAGD-genreAssignment.cls'}
results = {}

# label = 'genre'
path = './Dataset/LakhMatched/lmd_matched/lmd_matched/'
for label in tqdm(label_data.keys()):
    doc_path = 'Dataset/LakhMatched/Label/'+label_data[label]
    with open(doc_path,'r') as f:
        lines = f.readlines()

    res = []
    for line in lines:    
        music_ID, s = line.split('\t')
        if(os.path.exists(path+music_ID[2]+'/'+music_ID[3]+'/'+music_ID[4]+'/'+music_ID)):
            res.append([s[:-1], path+music_ID[2]+'/'+music_ID[3]+'/'+music_ID[4]+'/'+music_ID,music_ID])
    data = pd.DataFrame(res,columns=[label,'address','music_ID'])
    results[label] = data.copy()
    

sample_data = results['genre_more'].sample(frac = 1)

# for genre in results['genre_more']['genre_more'].unique():
#     sample_data = pd.concat([sample_data,results['genre_more'][results['genre_more']['genre_more'] == genre]])

bins_ = np.linspace(0, len(sample_data)+1, 10).astype(int)
for n in range(1,len(bins_)):
    music_data = get_pianoroll_data(sample_data.iloc[bins_[n-1]:bins_[n]], 0.1)
    # from scipy.ndimage import zoom
    # import pypianoroll
    # from pypianoroll import Multitrack, Track
    # music_data = []
    # for row in tqdm(sample_data.iterrows()):
    #     try:
    #         multitrack = pypianoroll.read(row[1].address + '/' + os.listdir(row[1].address)[0])
    #         channel = multitrack.stack().shape[0]
    #         height = int(multitrack.stack().shape[1]/multitrack.tempo[0][0]/24*600)
    #         res = np.zeros([channel,height, 128])
    #         a = multitrack.stack()
    #         res = zoom(a, (1, height/a[0].shape[0], 1))
    #         music_data.append([row[1].genre_more, row[1].music_ID, res])
    #     except:
    #         pass


    file=open("./music_sampel_data/music_data"+str(n)+".bin","wb")
    pickle.dump(music_data,file) #保存list到文件
    file.close()

# import os
# from os import system
 
# # 关机
# os.system("shutdown -s -t  60 ")