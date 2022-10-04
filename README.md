#Это телеграм-бот который ищет предметы на фотографии
_____
Для его развертывания был выбран бесплатный хостинг [DETA](https://web.deta.sh)

Про работу с DETA и деплой бота можно почитать [здесь](https://medium.com/@noufal.slm/create-your-own-telegram-bot-with-python-and-deta-sh-ef9aee7b93d5)

Про поиск предметов на картинке [здесь](https://habr.com/ru/post/678644/)
____
Для самого приложения пришлось разварачивать два микросервиса так как у DETA есть ограничения по памяти и на один он никак не хотел ставить opencv.

Теперь на одном работает хук, принимающий запросы из телеграма, а на другом yolo.

К слову картинки ищет он не идеально.

Еще проблема в том, что после обработки yolo, картинка никак не хочет конвертироваться в bytes, поэтому используется стороний сервис хостинга картинок на который картинки отправляются в формате base64.


Вот как это выглядит
![BIRD](https://github.com/IvanPermyakov/TelegramBotOnDeta/blob/main/Picture/Bird.JPG)

![FRUITS](https://github.com/IvanPermyakov/TelegramBotOnDeta/blob/main/Picture/Fruits.JPG)
