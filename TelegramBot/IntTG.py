import requests 
import os
from model.PhotoResponse import PhotoResp

token = os.environ['KEY']
base_url = "https://api.telegram.org/bot"
url_file = "https://api.telegram.org/file/bot"

def sendMessage(id, text):
    url = f"{base_url}{token}/sendMessage"
    requests.post(url, params={"chat_id": id, "text": text})

def getFile(file_id):
    url = f"{base_url}{token}/getFile?file_id={file_id}"
    res = requests.post(url)
    File = PhotoResp(res.json())
    urlphoto = F"{url_file}{token}/{File.result.file_path}"
    return urlphoto

def sendPhoto(id, urlPhoto):
    url = f"{base_url}{token}/sendPhoto"
    requests.post(url, params={"chat_id": id, "photo": urlPhoto})

def sendDocument(id, urlDocument):
    url = f"{base_url}{token}/sendDocument"
    requests.post(url, params={"chat_id": id, "document": urlDocument})