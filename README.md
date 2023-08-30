## Получение уведомлений о проверенных уроках

Telegram бот для получения уведомлений о проверенных уроках от обучающей платформы [devman](https://dvmn.org/)


### Необходимые требования

1. Токен [devman](https://dvmn.org/api/docs/)
2. Токен телеграм бота

[Как создать канал, бота и получить токен](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)

### Как установить

- Python3 должен быть уже установлен
- в директории с файлами программы необходимо создать `.env` файл, в котором прописать токены и Ваш персональный chat_id (можно получить, написав боту [@userinfobot](https://telegram.me/userinfobot)).
```
DEVMAN_API_TOKEN=thisistoKeN4example
TELEGRAM_TOKEN=6032470479:thisistoKeN4example
TG_CHAT_ID=123456789 
```
- Запустить телеграм бота командой **/start**

- Установить зависимости командой
```bash
pip install -r requirements.txt
```
### Как запустить

Запустить скрипт командой:
```bash
python3 main.py
```
данный скрипт запускает [long polling](https://dvmn.org/encyclopedia/about-chatbots/long-polling/) до сервера devman. В случае ответа преподавателя в телеграм придет ответ от бота.

