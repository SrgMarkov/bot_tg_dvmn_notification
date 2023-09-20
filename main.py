import logging
import os
import time

from dotenv import load_dotenv
import requests
from textwrap import dedent
from telegram import Bot

logger = logging.getLogger('Notification_bot')

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':
    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']

    headers = {'Authorization': f'Token {devman_token}'}
    params = {}

    bot = Bot(tg_token)
    connection_failure = False

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Bot is running')

    while True:
        try:
            long_polling_response = requests.get(LONG_POLLING_URL,
                                                 headers=headers,
                                                 params=params,
                                                 timeout=90)
            long_polling_response.raise_for_status()
            review_result = long_polling_response.json()
            if review_result['status'] == 'timeout':
                params['timestamp_to_request'] =\
                    review_result['timestamp_to_request']
            elif review_result['status'] == 'found':
                params['timestamp_to_request'] =\
                    review_result['last_attempt_timestamp']
                review_status = review_result['new_attempts'][0]
                lesson_tittle_text = f'''\
                                     У Вас проверили работу \
                                         "{review_status["lesson_title"]}"
                                     {review_status["lesson_url"]}

                                     '''
                if review_status['is_negative']:
                    negative_text = 'К сожалению, в работе нашлись ошибки.'
                    bot.send_message(chat_id=chat_id,
                                     text=dedent(lesson_tittle_text)
                                     + negative_text)
                else:
                    positive_text = 'Преподавателю всё понравилось.\
                        Можно приступать к следующему уроку!'
                    bot.send_message(chat_id=chat_id,
                                     text=dedent(lesson_tittle_text)
                                     + positive_text)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError as error:
            if not connection_failure:
                logger.error(f'Ошибка сетевого соединения {error}. \
                    Перезапуск бота')
                time.sleep(10)
                connection_failure = True
            else:
                logger.error(f'Ошибка сетевого соединения {error}. \
                    Перезапуск бота через 5 минут')
                time.sleep(300)
