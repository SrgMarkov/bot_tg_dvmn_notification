import os
from textwrap import dedent
from telegram import Bot
import requests
from dotenv import load_dotenv

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'

if __name__ == '__main__':
    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']

    headers = {'Authorization': f'Token {devman_token}'}
    params = {}

    bot = Bot(tg_token)
    while True:
        try:
            long_polling_response = requests.get(LONG_POLLING_URL, headers=headers, params=params)
            long_polling_response.raise_for_status()
            devman_server_response = long_polling_response.json()
            if devman_server_response['status'] == 'timeout':
                params['timestamp_to_request'] = devman_server_response['timestamp_to_request']
            elif devman_server_response['status'] == 'found':
                params['timestamp_to_request'] = devman_server_response['last_attempt_timestamp']
                review_status = devman_server_response['new_attempts'][0]
                lesson_tittle_text = f'''\
                                     У Вас проверили работу "{review_status["lesson_title"]}" 
                                     {review_status["lesson_url"]}
                                     
                                     '''
                if review_status['is_negative']:
                    negative_text = 'К сожалению, в работе нашлись ошибки.'
                    bot.send_message(chat_id=chat_id, text=dedent(lesson_tittle_text) + negative_text)
                else:
                    positive_text = 'Преподавателю всё понравилось. Можно приступать к следующему уроку!'
                    bot.send_message(chat_id=chat_id, text=dedent(lesson_tittle_text) + positive_text)
        except requests.exceptions.ReadTimeout as error:
            print(f'Ошибка: {error}')
        except requests.exceptions.ConnectionError as error:
            print(f'Прервано соединение: {error}')
