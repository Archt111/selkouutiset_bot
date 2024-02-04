import requests
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Token_ja_ID import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Constants
URL = 'https://yle.fi/selkouutiset'
COOKIE_CONSENT_NAME = 'accept-necessary-consents'
LIST_PATH = '//*[@id="yle__contentAnchor"]/div[1]/main/'
SEE_MORE_XPATH = '//button[contains(@class,"Buttonstyles__")]' #LIST_PATH + 'div[11]/button/span'
KAIKKI_BUTTON = '//*[@id="ukko-navbar-links"]/a[2]'
ARTICLE_HEADING = 'sc-aXZVg bdJlHI yle__article__heading yle__article__heading--1'
P_CLASS = 'aw-1gybjub aw-1p7kakr jxdWmn ilDxnw yle__article__paragraph'


def click_button(driver, check_type, value):
    try:
        locator = ()
        wait = WebDriverWait(driver, 10)
        if check_type == "name":
            # !!! Always double brackets for EC
           locator = (By.NAME, value)
           button = wait.until(EC.presence_of_element_located(locator))

        if check_type == "path":
            locator = (By.XPATH, value)
            button = wait.until(EC.presence_of_element_located(locator))
        
        button.click()
        wait.until(EC.invisibility_of_element_located(locator))
        print("Got it")
    except Exception as e:
        print(e)  


def iso_conversion(d_string, format) -> str:
    # Input format: dd.mm.yyyy
    return datetime.strptime(d_string, format).date()

def binary_search(array, wanted_time):
    matching_idx = 0

    low = 0
    high = len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_point = array[mid]

        if wanted_time == mid_point:
            print("Found matching date!")
            matching_idx = mid
            break
        elif wanted_time < mid_point:
            high = mid - 1
        else:
            low = mid + 1
    
    return matching_idx

def get_news(link_div):
    response = requests.get(link_div)   
    if response.status_code != 200:
        print("Failed")
        return None
    
    news = {}       
    soup = BeautifulSoup(response.text, 'html.parser') 
    titles = soup.find_all('h2', ARTICLE_HEADING)

    for title in titles:
        headline = title.get_text(strip = True)
        news[headline] = []
        paragraphs = title.find_all_next('p', P_CLASS)   
            
        for p in paragraphs:
            if p.find_previous('h2') != title:
                break
            news[headline].append(p.get_text(strip=True)) 
    
    return news

def processing_news(date):
    iso_formated = iso_conversion(date, "%d.%m.%Y")
    today_date = datetime.today().date()
    date_diff = today_date - iso_formated

    # If user wants news of other date, there's a need to scrape the web
    if(date_diff!=0):
        driver = webdriver.Edge()
        driver.get(URL)
        link_div = URL

        click_button(driver, "name", COOKIE_CONSENT_NAME)        
        click_button(driver, "path", KAIKKI_BUTTON)

        # Check the last date of the page to find the search space
        while True:
            #!!!! IMPROVEMENT NEEDED
            wait = WebDriverWait(driver, 10)
            time_elems = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "time")))
            time_values = [iso_conversion(time_elem.get_attribute("datetime")[:10], "%Y-%m-%d") 
                          for time_elem in time_elems]
            
            if iso_formated >= time_values[-1]: break
            click_button(driver, "path", SEE_MORE_XPATH) 
            
            
        # Search for the right article location
        if time_values[-1] != iso_formated:
            matching_idx = binary_search(time_values, iso_formated)
        else:
            matching_idx = -1
        
        # Find the parent class that contains this link to the article
        print(time_values[matching_idx])
        parent_div = time_elems[matching_idx].find_element(By.XPATH, LIST_PATH+'div[9]/div/div/div/div/div[1]')
        link_div = parent_div.find_element(By.XPATH, './h3/a').get_attribute('href')          
        driver.quit()

    return get_news(link_div)

        

async def send_to_telegram():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    chat_id = TELEGRAM_CHAT_ID
    news = processing_news("25.12.2023")

    if news:
        for title, content in news.items():
            paragraph = f"{title}\n\n" + "\n".join(content)
            await bot.send_message(chat_id, text=paragraph)
    else:
        await bot.send_message(chat_id, text="No news today :(")


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_to_telegram())