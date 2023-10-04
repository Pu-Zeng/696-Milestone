
from scipy.ndimage import zoom
import pypianoroll
from pypianoroll import Multitrack, Track
import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import mido
import string
import numpy as np

def get_pianoroll_data(sample_data, seconds_per_row):
    music_data = []
    for row in tqdm(sample_data.iterrows()):
        try:
            multitrack = pypianoroll.read(row[1].address + '/' + os.listdir(row[1].address)[0])
            channel = multitrack.stack().shape[0]
            height = int(multitrack.stack().shape[1]/multitrack.tempo[0][0]/multitrack.resolution*60/seconds_per_row)
            res = np.zeros([channel,height, 128])
            a = multitrack.stack()
            res = zoom(a, (1, height/a[0].shape[0], 1))
            program = [track.program for track in multitrack.tracks]
            music_data.append([row[1].genre_more, row[1].music_ID, program, res])
        except:
            pass
    return music_data


def get_full_data(sample_data):
    music_data = []
    for row in tqdm(sample_data.iterrows()):
        try:
            multitrack = pypianoroll.read(row[1].address + '/' + os.listdir(row[1].address)[0])
            # channel = multitrack.stack().shape[0]
            # height = int(multitrack.stack().shape[1]/multitrack.tempo[0][0]/multitrack.resolution*600)
            # res = np.zeros([channel,height, 128])
            a = multitrack.stack()
            # res = zoom(a, (1, height/a[0].shape[0], 1))
            program = [track.program for track in multitrack.tracks]
            # print(program)
            music_data.append([row[1].genre_more, row[1].music_ID, program, multitrack.tempo[0][0],multitrack.resolution, a])
        except:
            pass
    return music_data

def resize_data(a, tempo, resolution, seconds_per_row):
    try:
        height = int(a.shape[1]/tempo/resolution*60/seconds_per_row)
        res = zoom(a, (1, height/a[0].shape[0], 1))
        return res
    except:
        return None