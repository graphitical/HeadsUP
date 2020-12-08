import time
from typing import Dict
from ast import literal_eval
import numpy as np
import requests
import json
import cv2
import pathlib
import os
from pdf2image import convert_from_path
import sys
print(sys.executable)

# adapted from publaynet code

# constants
LAYOUT_API_URL = "http://17656761-ece1-4439-a212-ad15a95271e8.eastus2.azurecontainer.io/score"  # for PubLayNet
outputDir = 'images/'


def image_formatting(img):
    """
    It reduce the image size
    """
    shape = img.shape
    if img.shape[0] > 2000 or img.shape[1] > 2000:
        scale_percentage = int((2000 / img.shape[0]) * 100)
        width = int(img.shape[1] * scale_percentage / 100)
        height = int(img.shape[0] * scale_percentage / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img


def predict(image_path, LAYOUT_API_URL):
    """
    It predict the layout for the image and return dictionary
    return output is : 
    {
    'page_width': 1530,
    'page_height': 1980,
    'boxes':
        [
            {'label': 'text',
            'bbox': [768, 670, 1352, 836],
            'relative_box': [0.5019607843137255,
                0.3383838383838384,
                0.8836601307189542,
                0.4222222222222222]
            },
            {'label': 'table',
            'bbox': [769, 160, 1311, 651],
            'relative_box': [0.5026143790849673,
                0.08080808080808081,
                0.8568627450980392,
                0.3287878787878788]
            }
        ]
    }
    """
    image_path = open(image_path, 'rb').read()
    img = cv2.imdecode(np.frombuffer(image_path, np.uint8), -1)
    img = image_formatting(img)  # converts image to around 10 MB
    h, w, c = img.shape
    try:
        headers = {"Content-Type": "application/json"}
        # input_json is approx 50 MB in size
        input_json = json.dumps({"data": img.tolist()})
        for i in range(0, 3):  # number of tries = 3
            print("Layout inference: Calling publaynet try ", str(i+1))

            try:
                predictions = requests.post(
                    LAYOUT_API_URL, input_json, headers=headers, timeout=100)
                time.sleep(5*i)
                bbox = json.loads(predictions.content)
                if "boxes" in bbox:
                    break
            except Exception as ex:
                print("Layout inference: Error in publaynet call ", ex)

        del img
        return literal_eval(bbox)

    except Exception as ex:
        print("Layout inference: layout extraction using publaynet is failing", ex)


"""use below code with correct image path (PNG and JPG use im) to call this function - 
LAYOUT_API_URL = "http://17656761-ece1-4439-a212-ad15a95271e8.eastus2.azurecontainer.io/score"
predictions = predict ( image_path , LAYOUT_API_URL)
"""


def convert(file, outputDir):

    pdfTitle = file.replace('.pdf', '')
    print(pdfTitle)
    outputImageDir = os.path.join(outputDir, pdfTitle)
    pathlib.Path(outputImageDir).mkdir(parents=True, exist_ok=True)
    print(outputImageDir)
    pages = convert_from_path(file)
    counter = 1

    # print(pdfTitle)
    for page in pages:
        myfile = os.path.join(outputImageDir, pdfTitle +
                              '-page-' + str(counter)+'.png')
        counter = counter + 1
        page.save(myfile, "PNG")
        print(myfile)


def main():
    currentWorkingDirectory = os.getcwd()
    if len(sys.argv) < 2:
        print('usage: '+sys.argv[0]+' FILE_TO_CONVERT.pdf')
    else:
        file = sys.argv[1]
        convert(file, outputDir)
        if len(sys.argv) == 3:
            if sys.argv[2] != 'predict':
                print('invalid argument. use predict to predict')
                return
            print('predicting')
            imagesToBePredicted = []
            jsonOutputDir = '../predictions_json'
            PDFFileToBePredicted = sys.argv[1].replace('.pdf', '')
            sourceImageFolderPath = os.path.join(
                outputDir, PDFFileToBePredicted)
            for (dirpath, dirnames, filenames) in os.walk(sourceImageFolderPath):
                for fileName in filenames:
                    if fileName.endswith('.png'):
                        imagesToBePredicted.append(fileName)

            jsonOutputDir = os.path.join(jsonOutputDir, PDFFileToBePredicted)
            pathlib.Path(jsonOutputDir).mkdir(parents=True, exist_ok=True)
            #os.chdir(jsonOutputDir)
            #print('changed directory to '+os.getcwd())
            for image in imagesToBePredicted:
                pathToImage = os.path.join(sourceImageFolderPath, image)
                pathToImage = os.path.abspath(pathToImage)
                print('path to image is '+pathToImage)
                print('predicting image '+pathToImage)
                prediction = predict(pathToImage, LAYOUT_API_URL)
                print(prediction)
                with open(image+'.json','w') as f:
                    json.dump(prediction,f)


            os.chdir(currentWorkingDirectory)
            print('prediction done. switched back to '+os.getcwd())

                


if __name__ == "__main__":
    main()
