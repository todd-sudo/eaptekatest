from selenium import webdriver
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time


HEADLESS_MODE = False



def get_web_driver_options(proxy: dict = None) -> any:
    """Возвращает веб драйвер Firefox"""
    print("in driver func")

    options = webdriver.FirefoxOptions()
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    )
    options.set_preference("dom.webdriver.enabled", False)
    options.add_argument("--headless")
    # options.headless = HEADLESS_MODE

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('dom.webdriver.enabled', False)
    # profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0")
    root_path = os.getcwd()

    driver = webdriver.Firefox(
        executable_path=f"{root_path}/geckodriver",
        options=options,
        # seleniumwire_options=proxy,
        # firefox_profile=profile,
    )
    driver.set_page_load_timeout(3600 * 2 * 2)
    return driver
 


def main():


    driver = get_web_driver_options()
    # driver.implicitly_wait(5)
    
    try:
        url = "https://www.eapteka.ru/goods/id105320/"
        driver.get(url)

        time.sleep(3)
        print(driver.page_source)
        try:
            main_div = driver.find_element(By.CLASS_NAME, "sec-item-alt")
        except NoSuchElementException:
            raise Exception("Нет главного контейнера")
        try:
            name = main_div.find_element(By.TAG_NAME, "h1")
            name = name.text.strip()
        except NoSuchElementException:
            name = ""
        
        card_info = main_div.find_element(By.CLASS_NAME, "offer-card__info")
        ps = card_info.find_elements(By.TAG_NAME, "p")
        for p in ps:
            if "роизводитель" in p.text.strip():
                brand = p.find_element(By.TAG_NAME, "a").text.strip()
        try:
            price_old = card_info.find_element(By.CLASS_NAME, "offer-tools__old-price")
            price_old = int(price_old.text.strip().replace(" ", ""))
        except NoSuchElementException:
            price_old = 0
        try:
            price = card_info.find_element(By.CLASS_NAME, "offer-tools__price_num-strong")
            price = int(price.text.strip().replace(" ", ""))
        except NoSuchElementException:
            price = 0

        print(price)
        print(price_old)
        print(brand)
        print(name)
        
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


main()

