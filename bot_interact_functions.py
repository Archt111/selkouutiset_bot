import requests
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
from Token_ja_ID import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def get_news():
    url = 'https://yle.fi/selkouutiset'
    response = requests.get(url)
    
    if response.status_code == 200:
        news = {}

        soup = BeautifulSoup(response.text, 'html.parser') 
        #<h2 class="sc-aXZVg bdJlHI yle__article__heading yle__article__heading--1">       
        headers = soup.find_all('h2', class_='sc-aXZVg bdJlHI yle__article__heading yle__article__heading--1')

        for header in headers:
            title = header.get_text(strip = True)
            sentence = header.find_next('p')
            news[title] = []

            # <p class="aw-1gybjub aw-1p7kakr jxdWmn ilDxnw yle__article__paragraph"> 
            #while sentence.has_attr('class') and 'aw-1gybjub aw-1p7kakr jxdWmn ilDxnw yle__article__paragraph' in sentence['class']:
            while sentence and sentence.name == 'p':
                news[title].append(sentence.get_text(strip=True))
                sentence = sentence.find_next_sibling('p')

        return news
    else:
        print("Failed")
        return None

async def send_to_telegram():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    chat_id = TELEGRAM_CHAT_ID
    news = get_news()

    if news:
        for title, content in news.items():
            paragraph = f"{title}\n\n" + "\n".join(content)
            await bot.send_message(chat_id, text=paragraph)
    else:
        await bot.send_message(chat_id, text="No news today :(")


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_to_telegram())
        