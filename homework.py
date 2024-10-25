import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import requests
import random
import datetime
from newsapi import NewsApiClient

from googletrans import Translator

from config import TOKEN, NEWSAPI_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()
newsapi = NewsApiClient(api_key=NEWSAPI_API_KEY)

def info_date():
    today = datetime.date.today()
    month = today.strftime("%m")
    day = today.strftime("%d")

    url = f'http://numbersapi.com/{month}/{day}/date'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return(f"Не удалось получить данные: {response.status_code}")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\nНапиши команду /todate и я пришлю тебе интересный факт о сегодняшней дате. '
                         f'Или используй /news для получения свежей новости.')

@dp.message(Command('todate'))
async def todate(message: Message):
    info = info_date()
    info_splt = info.split()
    daymonth = ' '.join(info_splt[:2])
    translated_date = translator.translate(daymonth, src='en', dest='ru').text
    translated_info = translator.translate(info, src='en', dest='ru').text
    await message.answer(f'Итак сегодня {translated_date}.\n\nА вот и интересный факт про эту дату:\n\n{translated_info}')

@dp.message(Command('news'))
async def news(message: Message):
    # Получение новостей из России
    news_response = newsapi.get_top_headlines(page_size=10)
    articles = news_response.get('articles', [])


    if not articles:
        await message.answer("Не удалось получить новости.")
        return

    # Выбираем случайную новость
    article = random.choice(articles)
    title = article.get('title', 'Без заголовка')
    description = article.get('description', 'Без описания')
    url = article.get('url', '')

    news_message = (f"🗞 {translator.translate(title, src='en', dest='ru').text}\n\n"
                    f"{translator.translate(description, src='en', dest='ru').text}\n\n"
                    f"Читать подробнее: {url}")
    await message.answer(news_message)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
