import requests
from bs4 import BeautifulSoup
import re
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os


def get_all_url_image_site_brightside(url_site):
    response = requests.get(url_site)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text
    result = []

    text_script = str(soup.find_all("script"))
    text_script = text_script.split(title)[1].split('"type":"html"')
    for data in text_script:
        if '"subtype":"default","data":{"text"' in data and 'url' in data:
            try:
                link = re.findall('https://wl-brightside.cf.tsp.li/.{0,100}\.jpg', data)[0]
                des = data.split('"\\u003ch3')[1] \
                    .replace("\\u003c", "") \
                    .replace("em>", "") \
                    .replace('"', "") \
                    .replace("/", "") \
                    .replace("h3", "") \
                    .replace(">", "") \
                    .replace("style=\\text-align: center;\\", "") \
                    .split("}}")[0].strip()
                result.append([link, des])
            except:
                pass
    return title, result


def download_image_from_url(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def get_all_new_from_brightside():
    url = "https://brightside.me/"
    driver = webdriver.Firefox()
    driver.get(url)
    body = driver.find_element_by_css_selector('body')
    for i in range(200):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    links = driver.find_elements_by_xpath("//a[@href]")
    result = []
    for l in links:
        l = l.get_attribute('href')
        if "/comments" not in l and len(l) > 50 and "https://brightside.me/" in l:
            result.append(l)
    driver.close()
    return result


def save_image_from_brightside():
    root_path = '../../images/brightside.me'
    old_link_df = pd.read_csv("brightside.csv")
    old_links = old_link_df['link']
    new_links = get_all_new_from_brightside()
    df = old_link_df.append(pd.DataFrame({"link": new_links}))
    df.drop_duplicates(inplace=True)
    df.to_csv("brightside.csv", index=False)

    link_crawl = [link for link in new_links if link not in old_links]
    # link_crawl = [link for link in old_links]
    for link in link_crawl:
        title, urls = get_all_url_image_site_brightside(link)
        print(title, link)
        dir_path = os.path.join(root_path, title)
        if os.path.isdir(dir_path):
            pass
        else:
            os.mkdir(dir_path)

        for url, des in urls:
            print(des)
            print(url)
            file_path = os.path.join(dir_path, des)
            try:
                download_image_from_url(url, file_path)
            except:
                file_path = os.path.join(dir_path, des[:50])
                download_image_from_url(url, file_path)

save_image_from_brightside()