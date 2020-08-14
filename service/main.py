try:
    from youtube.service.download_image.app import get_all_url_image_site_brightside
    from youtube.service.reup_videos.app import gen_video_from_url_image
except:
    from download_image.app import get_all_url_image_site_brightside
    from reup_videos.app import gen_video_from_url_image
import pandas as pd
import platform
import git
import time




def gen_video(stt, title, link, intro):
    try:
        _, url_des = get_all_url_image_site_brightside(link)
        if platform.node() == "smile":
            title = f"Let's smile: Step {stt} {title}"
        elif platform.node() == "funpic":
            title = f"Funny pics: Step {stt} {title}"
        else:
            title = f"Funny pics: Step {stt} {title}"
        print(title)
        print(link)
        print(len(url_des))
        # for url in url_des:
        #     print(url, "\n")
        gen_video_from_url_image(url_des, title, intro)
        return True

    except Exception as e:
        print(f"Loi {e}")


def handle():
    if platform.node() == "funpic":
        links_df = pd.read_csv("funpic.csv")
        links_df['intro'] = "fun_pic"
    elif platform.node() == "smile":
        links_df = pd.read_csv("smile.csv")
        links_df['intro'] = "smile"
    else:
        FILES = ["funpic", "smile"]

        links_df = pd.DataFrame({"STT": [], "Title": [], "Link": [], "intro": []})
        for file in FILES:
            df = pd.read_csv(f"{file}.csv")
            df['intro'] = file
            links_df = links_df.append(df, ignore_index=True)
    links_df = links_df.sort_values(by=['STT'])
    loop_df(links_df)



def loop_df(df):
    for index, row in df.iterrows():
        reup_df = pd.read_csv("reup_list.csv")
        stt = row['STT']
        title = row['Title']
        link = row['Link']
        intro = row['intro']
        if (intro + " " + link) in reup_df["LINK"].to_list():
            continue
        if (gen_video(stt, title, link, intro)):
            reup_df = reup_df.append(pd.DataFrame({"LINK": [intro + " " + link]}))
        reup_df["LINK"].to_csv("reup_list.csv", index=False)
        if update_repo():
            handle()


def update_repo():
    g = git.cmd.Git()
    a = g.pull()
    if a == "Already up to date.":
        print("khong thay doi")
        return False
    else:
        print("co thay doi")
        return True

import os
handle()
os.system("zip -r videos.zip /home/vuhaibangtk/videos | "
          "rm -v /home/vuhaibangtk/videos | "
          "mv videos.zip /home/vuhaibangtk/videos")
while True:
    if update_repo():
        handle()
        os.system("zip -r videos.zip /home/vuhaibangtk/videos | "
                  "rm -v /home/vuhaibangtk/videos | "
                  "mv videos.zip /home/vuhaibangtk/videos")
    time.sleep(60*5)

