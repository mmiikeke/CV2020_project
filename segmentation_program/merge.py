#%%
import os
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from torchvision import transforms
from matplotlib import pyplot as plt
import segmentation_models_pytorch as smp
# !pip install segmentation_models_pytorch

def human_segmentation(image_path):
    base_path = Path(os.getcwd())
    
    # settings
    model_weights = base_path / 'segmentation_program' / 'model_pth' / '0104-weights.pth'
    img_name = image_path

    # model
    device = torch.device('cuda:0')
    model = smp.DeepLabV3('resnet50', in_channels=3, classes=1, activation='sigmoid')
    model.load_state_dict(torch.load(model_weights, map_location=device))
    model.eval()

    # transforms
    transform = transforms.Compose([
            transforms.Resize([256,256]),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    transform2 = transforms.Compose([
            transforms.Resize([256,256])
        ])

    # open image
    image = Image.open(img_name).convert('RGB')

    # get mask
    img_input = transform(image)
    img_input = torch.reshape(img_input, (1, 3, 256, 256))
    img_output = torch.round(model(img_input))

    # original image to tensor
    img_org = transform2(image)
    img_org = np.asarray(img_org)
    img_org = np.copy(img_org)
    img_org = torch.tensor(img_org)
    img_org = img_org.permute(2, 0, 1)
    img_org = torch.reshape(img_org, (1, 3, 256, 256))

    # remove background and convert to rgb
    result = img_org.byte() * img_output.byte()
    result = result.detach().numpy()[0]
    result = np.transpose(result, (1,2,0))
    result = Image.fromarray(result.astype('uint8')).convert('RGB')

    return result

def merge(background, portrait, bgw, bgh, imgw, imgh, x, y, scale=1):

    width1, height1 = background.size
    width2, height2 = portrait.size

    if scale != 1:
        width2 = width2 * scale
        height2 = height2 * scale
        portrait = portrait.resize((width2, height2))

    anchor_x = width1 - width2
    anchor_y = height1 - height2

    for w in range(width2):
        for h in range(height2):
            if int(w+x) >= 0 and int(h+y) >= 0 and int(w+x) < width1 and int(h+y) < height1:
                p = portrait.getpixel((w,h))
                if p != (0,0,0):
                    background.putpixel((int(w+x),int(h+y)), p)
    # background.save('result.png')
    return background


def segment_image(img_path):
    portrait = human_segmentation(img_path)

    portrait.save('tmp/out0.png')

    img = portrait.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("tmp/out1.png", "PNG")

    return portrait

def merge_image(human_path, bg_path, bgw, bgh, imgw, imgh, x, y):
    background = Image.open(bg_path).convert('RGB')
    human = Image.open(human_path).convert('RGB')
    image = merge(background, human, bgw, bgh, imgw, imgh, x, y)
    image.save('out.png')
    return image
