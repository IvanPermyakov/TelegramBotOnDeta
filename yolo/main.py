from flask import Flask, request
import numpy as np
import urllib.request
import cv2
import base64

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def read_route():
    return "Hello Deta"

@app.route("/json-example", methods = ['POST'])
def yolo():
    try:
        request_data = request.get_json()

        img_url = request_data['url']
            # Loading YOLO scales from files and setting up the network
        net = cv2.dnn.readNetFromDarknet("Resources/yolov4-tiny.cfg",
                                            "Resources/yolov4-tiny.weights")
        layer_names = net.getLayerNames()
        out_layers_indexes = net.getUnconnectedOutLayers()
        out_layers = [layer_names[index - 1] for index in out_layers_indexes]

        with open("Resources/coco.names.txt") as file:
            classes = file.read().split("\n")
        
        with open("Resources/coco.names.txt") as file:
            look_for = file.read().split("\n")

        list_look_for = []
        for look in look_for:
            list_look_for.append(look.strip())

        classes_to_look_for = list_look_for
        image = apply_yolo_object_detection(img_url, net, out_layers, classes, classes_to_look_for)
        image = cv2.imencode('.png', image)[1]
        '''
        В телеграм можно отправлять bytes и он сам должен открыть картинку
        Но тут проблема с этим
        UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
        Так и не нашел способа обойти это
        Поэтому использую Base64 и сторонний сервис для хостинга картинок
        img_arr = np.array(image, dtype="uint8")
        img_byte = img_arr.tobytes()
        '''
        img_byte = base64.b64encode(image).decode()
        return img_byte
    except Exception as e:
        return e
   

    
def apply_yolo_object_detection(image_to_process, net, out_layers, classes, classes_to_look_for):
    '''
    Приложение принимает ссылку на картинку
    Преобразовывает ее в картинку cv2   
    '''
    resp = urllib.request.urlopen(image_to_process)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 1 / 255, (608, 608),
                                (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(out_layers)
    class_indexes, class_scores, boxes = ([] for i in range(3))
    objects_count = 0

    for out in outs:
        for obj in out:
            scores = obj[5:]
            class_index = np.argmax(scores)
            class_score = scores[class_index]
            if class_score > 0:
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                obj_width = int(obj[2] * width)
                obj_height = int(obj[3] * height)
                box = [center_x - obj_width // 2, center_y - obj_height // 2,
                    obj_width, obj_height]
                boxes.append(box)
                class_indexes.append(class_index)
                class_scores.append(float(class_score))

    chosen_boxes = cv2.dnn.NMSBoxes(boxes, class_scores, 0.0, 0.4)
    for box_index in chosen_boxes:
        box_index = box_index
        box = boxes[box_index]
        class_index = class_indexes[box_index]

        if classes[class_index] in classes_to_look_for:
            objects_count += 1
            image_to_process = draw_object_bounding_box(image,
                                                        class_index, box, classes)

    final_image = draw_object_count(image_to_process, objects_count)
    return final_image


def draw_object_bounding_box(image_to_process, index, box, classes):
    
    x, y, w, h = box
    start = (x, y)
    end = (x + w, y + h)
    color = (0, 255, 0)
    width = 2
    final_image = cv2.rectangle(image_to_process, start, end, color, width)

    start = (x, y - 10)
    font_size = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = 2
    text = classes[index]
    final_image = cv2.putText(final_image, text, start, font,
                            font_size, color, width, cv2.LINE_AA)

    return final_image


def draw_object_count(image_to_process, objects_count):

    start = (10, 120)
    font_size = 1.5
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = 3
    text = "Objects found: " + str(objects_count)

    # Text output with a stroke
    # (so that it can be seen in different lighting conditions of the picture)
    white_color = (255, 255, 255)
    black_outline_color = (0, 0, 0)
    final_image = cv2.putText(image_to_process, text, start, font, font_size,
                            black_outline_color, width * 3, cv2.LINE_AA)
    final_image = cv2.putText(final_image, text, start, font, font_size,
                            white_color, width, cv2.LINE_AA)

    return final_image

    
    

