import cv2
import sys
import json

def crop(imageFileName, cropXStart,cropXEnd,cropYStart,cropYEnd):
    """crops the given image with the given bounding box coordinates."""
    print('cropping')
    print(type(cropXEnd))
    image = cv2.imread(imageFileName)
    croppedImage = image[cropXStart:cropXEnd,cropYStart:cropYEnd]
    cv2.imshow("cropped "+imageFileName,croppedImage)
    cv2.waitKey(0)
    return croppedImage

def main():
    cropped_images = list()
    if len(sys.argv) < 2:
        print('usage: image2text.py jsonFileName.jsonFileName')
    else:
        print("JSON file name",sys.argv[1])
        with open(sys.argv[1]) as f:
            data = json.load(f)
            category_id=0
            for category in data['categories']:
                if category['name'] == 'title':
                    category_id = category['id']
                    print("extracting text for category "+category['name'])
            annotations = []
            for annotation in data['annotations']:
                if annotation['category_id'] == category_id:
                    annotations.append(annotation)
            print('total number of title annotations:'+str(len(annotations)))
            #get images that have title annotations.

            
            for annotation in annotations:
                image_id = annotation['image_id']
                imageFileName = ''
                for image in data['images']:
                    if image['id'] == image_id:
                        imageFileName = image['file_name']
                boundingBox = annotation['bbox']
                print("cropping image"+str(image))
                cropYStart = int(boundingBox[0])
                cropYEnd = int(boundingBox[2])
                cropXStart = int(boundingBox[1])
                cropXEnd = int(boundingBox[3])
                print("bbox coordinates for image are "+str(boundingBox))
                cropped_image = crop(imageFileName,cropXStart,cropXEnd,cropYStart,cropYEnd)
                cropped_images.append(cropped_image)
            print('created total number of cropped images: '+str(len(cropped_images)))
        print('done cropping')
    print('exitting')

if __name__ == '__main__':
    main()
