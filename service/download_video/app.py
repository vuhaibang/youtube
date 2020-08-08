from pytube import YouTube
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time
from typing import List


def download_video_by_url(url, save_folder=None) -> None:
    "Download video from url with highest resolution"
    video = YouTube(url)
    path = '../../videos'
    if save_folder:
        path_video = os.path.join(path, "videos", save_folder)
        path_audio = os.path.join(path, "audio", save_folder)
    else:
        pass
    if os.path.isdir(path_video): pass
    else:
        os.mkdir(path_audio)
        os.mkdir(path_video)

    audio = video.streams.first()
    audio.download(path_audio)
    video = video.streams.get_highest_resolution().last()
    video.download(path_video)




def get_all_url_by_play_list(url_play_list) -> List:
    driver = webdriver.Firefox()
    driver.get(url_play_list)
    body = driver.find_element_by_css_selector('body')
    class_name_videos = "ytd-playlist-video-list-renderer"
    url_format = r"^(https|http)(://)(www.youtube.com/watch)"
    num_videos = 0
    while True:
        for i in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        new_num_videos = len(driver.find_elements_by_class_name(class_name_videos))
        if new_num_videos == num_videos:
            break
        else:
            num_videos = new_num_videos
    url_videos = []
    for e in driver.find_elements_by_xpath("//a[@href]"):
        href = e.get_attribute('href')
        if re.match(url_format, href):
            url_videos.append(href)
    driver.close()
    url_videos = list(set(url_videos))
    return url_videos


if __name__ == '__main__':
    # url = "https://www.youtube.com/playlist?list=UUSnVteUNlhr1SqCjTQx0PDQ&amp;feature=applinks"
    # url_videos = get_all_url_by_play_list(url)
    # for video in url_videos:
    #     download_video_by_url(video, save_folder="St319")
    url = "https://www.youtube.com/watch?v=XAdyTSprtgA&list=UUSnVteUNlhr1SqCjTQx0PDQ&index=80&t=0s"
    download_video_by_url(url, save_folder="St319")
