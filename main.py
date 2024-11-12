import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Функция для скачивания контента по URL
def download_file(url, folder):
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
    
    # Проверим, существует ли файл с таким же именем
    if os.path.exists(local_filename):
        print(f"Файл {local_filename} уже существует, пропускаем.")
        return

    # Скачать файл
    print(f"Скачиваю: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Проверка успешного ответа
    with open(local_filename, 'wb') as f:
        f.write(response.content)

# Функция для парсинга HTML и скачивания ресурсов
def download_site(url, folder):
    # Создаем папку, если ее нет
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Получаем HTML страницы
    print(f"Парсим страницу {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Скачиваем CSS, JavaScript, изображения и другие ресурсы
    for tag in soup.find_all(['link', 'script', 'img']):
        if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
            href = tag.get('href')
            if href:
                download_file(urljoin(url, href), folder)
        elif tag.name == 'script' and tag.get('src'):
            src = tag.get('src')
            if src:
                download_file(urljoin(url, src), folder)
        elif tag.name == 'img' and tag.get('src'):
            src = tag.get('src')
            if src:
                download_file(urljoin(url, src), folder)

    # Скачиваем сам HTML код страницы
    with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

# Замените на URL вашего сайта
url = 'https://www.youtube.com/watch?v=0FdSTRq36iU'
folder = 'downloaded_site'

download_site(url, folder)
