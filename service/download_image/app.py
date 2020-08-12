import requests
from bs4 import BeautifulSoup
import re
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import cv2
import sqlite3


def get_all_url_image_site_brightside(url_site):
    response = requests.get(url_site)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text
    result = []

    text_script = str(soup.find_all("script"))
    text_script = text_script.split(title)[1]
    text_script = text_script.split('"type":"html"')
    for data in text_script:
        if '"subtype":"default","data":{"text"' in data and 'url' in data:
            try:
                link = re.findall('https://wl-brightside.cf.tsp.li/.{0,100}\.jpg', data)[0]
                des = data.split('"\\u003c')[1]\
                    .split("}}")[0]
                des = re.sub(r"h3 style[^\s]*|\\u0.{0,10}\>|center;\\\"\>|\\u00[^\s]*|href=[^\s]*|target=[^\s]*|\\n|"
                             r"ul>|h[0-9]>|p\>|h[0-9] align=[^\s]*|\&quot\;|\&\#[^\s]*|h3.class\=[^\s]+|style\=[^\s]+", "", des)\
                    .strip().strip('"').strip("'")
                des = re.sub(r"\s+", " ", des)
                des = re.sub(r"^[0-9]+\s{0,1}\.", "",des)
                des = des.strip().strip("'").strip('"')
                result.append([link, des])
            except Exception as e:
                print(e)
            continue
        try:
            if len(result[-1][1]) > 0 and len(result[-1][1]) < 4:
                data = re.sub(r"\\u003ca.*\\u003c\/a\>", "", data)
                data = re.findall(r"\\u003cp\>(.*)\\u003c\/p\>", data)[0]
                data = re.sub(r"h[0-9] style[^\s]*|\\u0.{0,10}\>|center;\\\"\>|\\u00[^\s]*|href=[^\s]*|target=[^\s]*|"
                              r"\\n|ul>|h[0-9]>|p\>|h[0-9] align=[^\s]*|\&quot\;|h3.class\=[^\s]+|style\=[^\s]+", "", data)\
                    .strip().strip('"').strip("'")
                data = re.sub(r"\s+", " ", data)
                result[-1][1] += data
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
    for i in range(10):
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
    links = get_all_new_from_brightside()
    # links = ["https://brightside.me/wonder-films/15-facts-about-the-princess-diaries-that-will-make-you-fall-in-love-with-the-movie-all-over-again-798356/"]
    for link in links:
        if (check_sqlite("news", link, conn)):
            print("Value exits")
            continue
        title, urls = get_all_url_image_site_brightside(link)
        insert_sqlite("news", (link, title), conn)
        print(f"Insert news {link} {title}")

        id_news = str(select_sqlite("news", link, conn)[0])
        dir_path = os.path.join(root_path, id_news)
        if os.path.isdir(dir_path):
            pass
        else:
            os.mkdir(dir_path)

        for url, des in urls:
            print(des)
            print(url)
            if (check_sqlite("images", url, conn)):
                print("Value exits")
                continue
            insert_sqlite("images", (url, des), conn)
            print(f"Insert news {url} {des}")
            id_images = str(select_sqlite("images", url, conn)[0])
            file_path = os.path.join(dir_path, id_images + ".png")
            download_image_from_url(url, file_path)


def check_sqlite(table, value, conn):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE url=(?)", ([value]))
    result = cur.fetchall()
    cur.close()
    return result


def insert_sqlite(table, value, conn):
    cur = conn.cursor()
    sql = f'INSERT INTO {table}(url,des) VALUES(?,?)'
    cur.execute(sql, value)
    conn.commit()
    cur.close()


def select_sqlite(table, value, conn):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE url=(?)", ([value]))
    row = cur.fetchall()
    cur.close()
    return row[0]


def resize_image(path):
    src = cv2.imread(path)
    height = 1080
    width = min(1900, int(src.shape[1] * 1080 / src.shape[0]))
    dsize = (width, height)
    output = cv2.resize(src, dsize)
    cv2.imwrite(path, output)


# save_image_from_brightside()
if __name__ == '__main__':
    conn = sqlite3.connect(
        '/home/vhb/PycharmProjects/Project/youtube/database/brightside.db')
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(1024, 768))
    display.start()

    for link in get_all_new_from_brightside():
        print(link)
        for des in get_all_url_image_site_brightside(link)[1]:
            print(des)
