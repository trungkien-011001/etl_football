from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc
import psycopg2
import pandas as pd
import re
from typing import List,Dict
import time
import random
import logging

BASE = 'https://www.transfermarkt.com/'

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)

def smart_sleep(min_s=3, max_s=6):
    time.sleep(random.uniform(min_s,max_s))

def load_homepage():
    global driver

    try:

        # Setup for handling -> lightweight anti-bot measures (a form of basic anti-scraping defense) where fields are sometimes returned as null values on the first load, but become available after repeated page refreshes.”
        options = Options()
        options.add_argument("headless--new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(
            options=options,
            browser_executable_path="/usr/bin/google-chrome",
            driver_executable_path="/usr/local/bin/chromedriver",
            use_subprocess=False
            )
        logger.info("Chrome started successfully!")

        driver.get(BASE)

    except Exception as e:
         logger.info(f"Error when loading homepage: {e}")

def end_session():
     global driver
     driver.quit()

def accept_cookies_if_present(driver):
        # Wait for iframe and switch
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='consent']"))
            )
            driver.switch_to.frame(iframe)

            # Click the button
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Accept & continue']"))
            )
            button.click()

            driver.switch_to.default_content()

        except:
             None

def fetch_with_backoff(driver, url, base_wait=0.25):
    """
    Function for multiple retries when the page encounters error 403
    """
    
    attempt = 1

    driver.get(url)
    accept_cookies_if_present(driver)

    while True:
        driver.get(url)
        page_source = driver.page_source

        if 'forbidden' in page_source:
            wait = base_wait * (2 ** (attempt-1))
            jitter = random.uniform(0, wait * 0.5)
            total_wait = wait + jitter
            time.sleep(total_wait)
            attempt += 1
        else:
            return True
        
def safe_get_text(by, selector, index=None, strip=True) -> str:
    """
    Getting text from html elements safely if not found or out of index

    *Args:
        1. by: Type of html selection (CSS_SELECTOR, XPATH, CLASS_NAME....)
        2. selector: strings contain html element (div, a, span....)
        3. index: Indexes of the selected elements (use only for find_elements)
        4. strip: True for stripping text, False for no Text-stripping
    """
    value = None

    try:
        if index is None:
            el = driver.find_element(by, selector)
            return el.text.strip() if strip else el.text
        else:
            els = driver.find_elements(by, selector)
            if len(els) > index:
                return els[index].text.strip() if strip else els[index].text
    except Exception as e:
        return None


def safe_get_attribute(by, selector, attribute=str, strip=True) -> str:
    """
    Getting text of attribute from html elements (img, src....) safely if not found or out of index

    *Args:
        1. by: Type of html selection (CSS_SELECTOR, XPATH, CLASS_NAME....)
        2. selector: strings contain html element (div, a, span....)
        3. attribute: str name of the attribute
        4. strip: True for stripping text, False for no Text-stripping
    """

    try:
        if attribute:
            el = driver.find_element(by, selector)
            return str(el.get_attribute(attribute)).strip()
        else:
            None
    except Exception as e:
        return None

def get_player_info(player_urls: List) -> pd.DataFrame:
    """
    Return a DataFrame of footballers information from a List of player urls
    """

    logger.info("Starting fetching PLAYER data....")

    players = []

    # Accept cookie at the first url
    fetch_with_backoff(driver, player_urls[0])
    accept_cookies_if_present(driver)

    # Scape the data for the rest
    try:
        for player_url in player_urls:
            smart_sleep(min_s=1.2, max_s=3)
            fetch_with_backoff(driver, player_url)

            citizenship = None
            attempt = 1
            while not citizenship:
            # information
                headline_name = safe_get_text(By.CSS_SELECTOR, 'h1.data-header__headline-wrapper')
                club = safe_get_text(By.CSS_SELECTOR, 'span[class="data-header__club"]')
                league = safe_get_text(By.CSS_SELECTOR, 'span[class="data-header__league"]')
                dob_age = safe_get_text(By.CSS_SELECTOR ,'span[itemprop="birthDate"]')
                place_of_birth = safe_get_attribute(By.CSS_SELECTOR ,'li.data-header__label img', attribute='title')
                citizenship = safe_get_text(By.CSS_SELECTOR, 'span[itemprop = "nationality"]')
                height = safe_get_text(By.CSS_SELECTOR, 'span[itemprop="height"]')

                position = driver.find_elements(By.CSS_SELECTOR, 'div.data-header__details li.data-header__label')[2].text
                if 'Position: ' not in position:
                    position = driver.find_elements(By.CSS_SELECTOR, 'div.data-header__details li.data-header__label')[3].text
                    if 'Position: ' not in position:
                        position = driver.find_elements(By.CSS_SELECTOR, 'div.data-header__details li.data-header__label')[4].text
                    
                market_value_wrapper = safe_get_text(By.CSS_SELECTOR, 'div.data-header__box--small a.data-header__market-value-wrapper')
                link = player_url
                attempt +=1

                # Append to Dict
                player_dict = {
                    'headline_name': headline_name,
                    'club': club,
                    'league': league,
                    'dob_age': dob_age,
                    'place_of_birth': place_of_birth,
                    'citizenship': citizenship,
                    'height': height,
                    'position': position,
                    'market_value_wrapper': market_value_wrapper,
                    'link': link
                }

                if not citizenship:
                    driver.refresh()
                    smart_sleep(min_s=0.5, max_s=1.5)
                else:
                    break

            # Append player info to List
            players.append(player_dict)
            logger.info(f"Extracted {len(players)}/{len(player_urls)} player(s)")
            
    except WebDriverException as e:
        logger.info("WebDriverException: ", e)

        # Change to DataFrame
    df = pd.DataFrame(players)
    
    print(df.info())

    return df

#============================ Data Pipline =================================
def load_to_postgre(df: pd.DataFrame, table_name: str):
    conn = psycopg2.connect(
        host = 'host.docker.internal',
        port=5432,
        dbname = 'football',
        user = 'postgres',
        password = 'postgres'
    )

    cur = conn.cursor()

    cur.execute(f"""
        TRUNCATE TABLE players.{table_name};
                """)

    for _, row in df.iterrows():
        cur.execute(f"""
            INSERT INTO players.{table_name}
            (headline_name, club, league, dob_age, place_of_birth, citizenship, height, position, market_value_wrapper, link) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (
            row['headline_name'],
            row['club'],
            row['league'],
            row['dob_age'],
            row['place_of_birth'],
            row['citizenship'],
            row['height'],
            row['position'],
            row['market_value_wrapper'],
            row['link'],
        ))

    logger.info("Loading to Postgres successfully")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":

    try:
        load_homepage()
        df_pl = get_player_info(['https://www.transfermarkt.com/david-raya/profil/spieler/262749', 'https://www.transfermarkt.com/kepa-arrizabalaga/profil/spieler/192279'])
        load_to_postgre(df=df_pl, table_name="test_raw")
        end_session()

    except Exception as e:
        logger.info(e)