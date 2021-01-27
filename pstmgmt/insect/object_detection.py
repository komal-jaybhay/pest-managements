import cv2
import numpy as np
import os
from pathlib import Path
from urllib.request import urlopen

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    # return the image
    return image


def get_insects(path, media_root, from_number, uuid):
    # import pdb;pdb.set_trace()
    weight_file = os.path.join(os.path.dirname(__file__), 'yolov3_training_10000.weights')
    cfg_file = os.path.join(os.path.dirname(__file__), 'yolov3_testing.cfg')
    net = cv2.dnn.readNet(weight_file, cfg_file)
    classes = []
    with open(os.path.join(os.path.dirname(__file__), 'classes.txt'),'r') as f:
        classes = f.read().splitlines()

    #img = cv2.imread('C:/Users/Lenovo/Desktop/yolov3/Test_Images/spider6.jpg')
    img = url_to_image(path)#cv2.imread(path)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

    # for b in blob:
    #     for n, img_blob in enumerate(b):
    #         cv2.imshow(str(n), img_blob)

    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes=[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    #print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    # print(indexes.flatten())
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    insects = ""
    label = []
    if len(indexes) > 0:
        # import pdb;
        # pdb.set_trace()
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            class_name = str(classes[class_ids[i]])
            if class_name not in label:
                label.append(class_name)

            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            print(label)
            cv2.putText(img, class_name + " " + confidence, (x, y+20), font, 2, (0, 255, 0), 2)

        insects = ', '.join(label)
    # import pdb;pdb.set_trace()
    basename = os.path.basename(path)
    ext = Path(basename).suffix
    name = ''.join(['output', ext])
    filename = os.path.join(media_root, 'insects', from_number, str(uuid), 'images', name)
    cv2.imwrite(filename, img)
    # with open(filename, 'wb') as f:
    #     f.write(img)
    return insects, label
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
