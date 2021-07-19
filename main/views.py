from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import numpy as np
from PIL import Image
import json
import io
import os
from keras.models import load_model
from utils.utils import get_yolo_boxes, makedirs
from utils.bbox import draw_boxes
from .forms import ImageForm
from  .models import Image as ImageModel

# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            filelist = os.listdir('main/media/')
            for f in filelist:
                os.remove(os.path.join('main/media/', f))
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            imagefile = request.FILES['file']
            imagefile_array = np.array(Image.open(imagefile))
            new_img = predict(image=imagefile_array)
            fs = FileSystemStorage()
            fs.save(imagefile.name, new_img)
            img_obj = '../main/media/' + imagefile.name
            return render(request, 'Home.html', {'img_obj': img_obj})
        except:
            print('Ошибка!')
            return render(request, 'Home.html')
    else:
        return render(request, 'Home.html')

def predict(image):
    with open('config.json') as config_buffer:
        config = json.load(config_buffer)

    ###############################
    #   Set some parameter
    ###############################
    net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
    obj_thresh, nms_thresh = 0.5, 0.45

    ###############################
    #   Load the model
    ###############################
    os.environ['CUDA_VISIBLE_DEVICES'] = config['train']['gpus']
    infer_model = load_model(config['train']['saved_weights_name'])

    ###############################
    #   Predict bounding boxes
    ###############################

    # predict the bounding boxes
    boxes = get_yolo_boxes(infer_model, [image], net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)[0]

    # draw bounding boxes on the image using labels
    draw_boxes(image, boxes, config['model']['labels'], obj_thresh)

    # output the image with bounding boxes to file
    img = Image.fromarray(image)

    # create file-object in memory
    file_object = io.BytesIO()

    # write PNG in file-object
    img.save(file_object, 'PNG')

    # move to beginning of file so `send_file()` it will read from start
    file_object.seek(0)

    return file_object