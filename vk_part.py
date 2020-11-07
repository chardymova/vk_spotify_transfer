'''Собираем данные формата: "Имя исполнителя Песня" с плейлиста, к которому у нас есть доступ.
Требуется авторизация вк. Данные должны быть указаны в файле variables.'''

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from variables import phone_number, password, target_audio_link


def log_in_vk(browser):
    '''Авторизовываемся в вк, используя данные, указанные в файле variables.py.'''
    time.sleep(4)
    browser.find_element(By.CSS_SELECTOR, '#email').send_keys(phone_number)
    browser.find_element(By.CSS_SELECTOR, '#pass').send_keys(password)
    browser.find_element(By.CSS_SELECTOR, '#login_button').click()
    return browser


def collection_audio_list(browser):
    '''Возвращаем список, где каждый элемент Имя исполнителя и Название трека.'''
    selector_artist_name = '.audio_page__rows_wrap div.audio_row__performers'
    selector_title_name = '.audio_page__rows_wrap div.audio_row__title'
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    artist_list = browser.find_elements(By.CSS_SELECTOR, selector_artist_name)
    title_list = browser.find_elements(By.CSS_SELECTOR, selector_title_name)
    song_list = []
    for i, item in enumerate(artist_list):
        song = item.text + ' ' + title_list[i].text
        song_list.append(song)
    return song_list


def main():
    browser = webdriver.Chrome()
    browser.get(target_audio_link)
    auth_vk = log_in_vk(browser)
    time.sleep(4)
    auth_vk.get(target_audio_link)
    song_list = collection_audio_list(auth_vk)
    browser.quit()
    return song_list


if __name__ == '__main__':
    main()
