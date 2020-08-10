try:
    from youtube.service.download_image.app import get_all_url_image_site_brightside
    from youtube.service.reup_videos.app import gen_video_from_url_image
except:
    from download_image.app import get_all_url_image_site_brightside
    from reup_videos.app import gen_video_from_url_image

import pandas as pd

links_df = pd.read_csv("brightside_url.csv")['link']
for link in links_df:
    print(link)
    try:
        title, url_des = get_all_url_image_site_brightside(link)
    except:
        continue
    print(len(url_des))
    # gen_video_from_url_image(url_des, title)
