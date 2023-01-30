from __future__ import print_function
import os
import torch
from torch.utils.data import DataLoader

from Dataset.dataset_io.torchneuromorphic.dvs_gestures import dvsgestures_dataloaders


def load_data(dataset, num_workers, ds, dt, T, batch_size):
    path = './Dataset/dataset/'
    if dataset == 'DVS128-Gesture':
        # manually download from https://www.research.ibm.com/dvsgesture/ 
        # and place under dataset/DVS128-Gesture/
        # create_events_hdf5('./dataset/DVS128-gesture/DvsGesture',
        #'./dataset/DVS128-gesture/dvs128-gestures.hdf5')
        root = path  + dataset + '/dvs128-gestures.hdf5'        
        train_dl, test_dl= dvsgestures_dataloaders.create_dataloader(
        root= root,
        batch_size=batch_size,
        chunk_size_train = T,
        chunk_size_test = T,
        ds=ds,
        dt=dt*1000,
        num_workers=num_workers,
        sample_shuffle=True,
        time_shuffle=False,
        drop_last=True)
        
    elif dataset == 'N-Cars':
        root = path  + dataset + '/Prophesee_Dataset_n_cars' 
        # manually download from https://www.prophesee.ai/2018/03/13/dataset-n-cars/
        # and place under dataset/N-Cars
        train_ds = prophesee_ncars.PropheseeNCars(root, is_train=True, transforms=ToDense(dt*ms))
        test_ds = prophesee_ncars.PropheseeNCars(root, is_train=False, transforms=ToDense(dt*ms))
        train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, drop_last=True)
        test_dl = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, drop_last=True)
        
    elif dataset == 'SHD':
        root = path  + dataset
        train_ds = spikedata.SHD(root, dt=dt*1000, num_steps=T, train=True)
        test_ds = spikedata.SHD(root, dt=dt*1000, num_steps=T, train=False)
        train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, drop_last=True)
        test_dl = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, drop_last=True)
    
    return train_dl, test_dl