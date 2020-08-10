from youtube.service.download_image.app import get_all_url_image_site_brightside
from youtube.service.reup_videos.app import gen_video_from_url_image


link = "https://brightside.me/wonder-films/15-facts-about-the-princess-diaries-that-will-make-you-fall-in-love-with-the-movie-all-over-again-798356/"
title, url_des = get_all_url_image_site_brightside(link)
gen_video_from_url_image(url_des, title)
