# -*- coding: utf-8 -*-
import os 

# pytorch imports
import torch
import torchvision
from torchvision import datasets, models, transforms
from torchvision import transforms, utils

from PIL import Image


import cxrnet.visualize_prediction as V

import pandas as pd

import matplotlib.pyplot as plt
plt.switch_backend('Agg')

import seaborn as sns

import numpy as np


#suppress pytorch warnings about source code changes
import warnings
warnings.filterwarnings('ignore')

FINDINGS = [
        'Atelectasis',
        'Cardiomegaly',
        'Effusion',
        'Infiltration',
        'Mass',
        'Nodule',
        'Pneumonia',
        'Pneumothorax',
        'Consolidation',
        'Edema',
        'Emphysema',
        'Fibrosis',
        'Pleural_Thickening',
        'Hernia']

def find_pred_one(img_path, labels=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    PATH_TO_MODEL = os.path.join(dir_path, "pretrained/checkpoint")
    
    # load model
    checkpoint = torch.load(PATH_TO_MODEL, map_location=lambda storage, loc: storage)
    model = checkpoint['model']
    del checkpoint
    model.cpu()

    # load image
    image = Image.open(img_path)
    image = image.convert('RGB')

    # preprocess 
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    preprocess = transforms.Compose([
        transforms.Scale(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    
    img_tensor = preprocess(image)
    img_tensor.unsqueeze_(0)
    
    # forward pass on model
    
    # create predictions for label of interest and all labels
    pred = model(torch.autograd.Variable(img_tensor.cpu())).data.numpy()[0]
    predx = ['%.3f' % elem for elem in list(pred)]
    
    cxr = img_tensor.numpy().squeeze().transpose(1,2,0)    
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    cxr = std * cxr + mean
    cxr = np.clip(cxr, 0, 1)
    
    pred_col = ["Finding","Predicted Probability"]
    if (labels):
        preds_concat=pd.concat([pd.Series(FINDINGS),pd.Series(predx),pd.Series(labels.numpy().astype(bool)[0])],axis=1)
        pred_col.append("Ground Truth")
    else:
        preds_concat=pd.concat([pd.Series(FINDINGS),pd.Series(predx)],axis=1)
    preds = pd.DataFrame(data=preds_concat)
    preds.columns=pred_col
    preds.set_index("Finding",inplace=True)
    preds.sort_values(by='Predicted Probability',inplace=True,ascending=False)
    
    return (preds, cxr, img_tensor, model)


def show_pred_one(preds, cxr, img_tensor, model, label_index, fdir):
    LABEL = preds.index[label_index]
    
    fig = plt.figure()
    
    raw_cam = V.calc_cam(img_tensor, LABEL, model)
    hmap = sns.heatmap(raw_cam.squeeze(),
            cmap = 'viridis',
            alpha = 0.3, # whole heatmap is translucent
            annot = True,
            zorder = 2,square=True,vmin=-5,vmax=5
            )
                
    hmap.imshow(cxr,
          aspect = hmap.get_aspect(),
          extent = hmap.get_xlim() + hmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    hmap.axis('off')
    hmap.set_title("P("+LABEL+")="+str(preds['Predicted Probability'][label_index]))
    
    fn = str(LABEL)+"_P"+str(preds['Predicted Probability'][label_index])+"_file.png"
    plt.savefig(os.path.join(fdir, fn), transparent=True)
    plt.close(fig)
    return fn

def get_pred(fdir):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    
    
    data = np.load(os.path.join(dir_path, 'thresholds.npy'))
    print(data)
    
    STARTER_IMAGES=True
    PATH_TO_IMAGES = os.path.join(dir_path, "starter_images/")
    
    #STARTER_IMAGES=False
    #PATH_TO_IMAGES = "your path to NIH data here"
    PATH_TO_MODEL = os.path.join(dir_path, "pretrained/checkpoint")
    LABEL="any"
    
    
    POSITIVE_FINDINGS_ONLY=False
    
    dataloader,model= V.load_data(PATH_TO_IMAGES,LABEL,PATH_TO_MODEL,POSITIVE_FINDINGS_ONLY,STARTER_IMAGES)
    print("Cases for review:")
    print(len(dataloader))
    
    
    
    LABEL = FINDINGS[0]
    
    [preds, cxr, inputs] = V.show_next(dataloader,model, LABEL)
    print(preds)
    LABEL = preds.index[0]
    
    fig, (showcxr,heatmap) =plt.subplots(ncols=2,figsize=(14,5))
    #plt.imshow(cxr)
    #plt.show()
    
    label_index = next(
            (x for x in range(len(FINDINGS)) if FINDINGS[x] == LABEL))
    
    raw_cam = V.calc_cam(inputs, preds.index[0], model)
    hmap = sns.heatmap(raw_cam.squeeze(),
            cmap = 'viridis',
            alpha = 0.3, # whole heatmap is translucent
            annot = True,
            zorder = 2,square=True,vmin=-5,vmax=5
            )
                
    hmap.imshow(cxr,
          aspect = hmap.get_aspect(),
          extent = hmap.get_xlim() + hmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    hmap.axis('off')
    hmap.set_title("P("+LABEL+")="+str(preds['Predicted Probability'][label_index]))
    
    showcxr.imshow(cxr)
    showcxr.axis('off')
    showcxr.set_title("original image")
    
    fn = str(LABEL)+"_P"+str(preds['Predicted Probability'][label_index])+"_file.png"
    plt.savefig(os.path.join(fdir, fn))
    return (preds, fn)

if __name__ == '__main__':
    #[preds, fn] = get_pred('')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir_path, "starter_images", "00000075_000.png")
    print(img_path)
    [preds, cxr, img_tensor, model] = find_pred_one(img_path)
    fn = show_pred_one(preds, cxr, img_tensor, model, 0, '')
    print(fn)