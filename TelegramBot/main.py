import os
import requests 
from fastapi import FastAPI
from fastapi.requests import Request
from model.context import Context
from model.enums import dispatches, try_enum
from IntTG import *

IMGBBtoken = os.environ['IMGBBKEY']
YOLOURL = os.environ['YOLOURL'] #https://То что находится здесь.deta.dev/json-example - 

app = FastAPI()

@app.get("/")
async def read_route():
    return "Hello Deta"

@app.post("/")
async def handler(request: Request):
    sender = Context(await request.json())
    if sender.type is not dispatches.unknown:
        sender.message
        msg = sender.message
        chat_id = msg.chat.id
        text = msg.text
        try:
            if msg.document:
                Photo = msg.document.file_id
                sendDocument(chat_id, Photo)
            elif msg.photo:
                NamePhoto = msg.photo[2].file_unique_id
                Photo = msg.photo[2].file_id
                urlphoto = getFile(Photo) 
                #Отправка ссылки на картинку, в ответ получаем base64
                byte_to_image = sendToYolo(urlphoto)
                #Отправка base64 в хостинг картинок, в ответ получаем ссылку на картинку
                answer = sendPhotoToIMGBB(byte_to_image.text, NamePhoto)
                urlIMGBB = answer.json()['data']['image']['url']
                #Отправляем обработанную картинку в чат
                sendPhoto(chat_id, urlIMGBB)
        except Exception as e:
            sendMessage(chat_id, e)

def sendToYolo(urlphoto):
    url = f'https://{YOLOURL}.deta.dev/json-example'
    head = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    byte_to_image = requests.post(url, json={'url': urlphoto}, headers=head)
    return byte_to_image

def sendPhotoToIMGBB(byte_to_image, name):
    url = f"https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBBtoken,
        "name": name,
        "image": byte_to_image,
    }
    res = requests.post(url, payload)
    return res

