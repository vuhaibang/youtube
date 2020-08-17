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
import random



def gen_video(stt, title, link, intro):
    try:
        _, url_des = get_all_url_image_site_brightside(link)
        if platform.node() == "smile":
            title = f"Let's smile: Step {stt} {title}"
        elif platform.node() == "funpic":
            title = f"Funny pics: Step {stt} {title}"
        else:
            DICT = {"funpic": "Funny pics",
                    "smile": "Smile pics",
                    "dailyjoy": "Daily joy",
                    "findingjoy": "Finding Joy",
                    "happymonkey": "Happy Monkey"}
            title = f"{DICT[intro]}: Step {stt} {title}"
        print(title)
        print(link)
        print(len(url_des))
        # for url in url_des:
        #     print(url, "\n")
        random.shuffle(url_des)
        gen_video_from_url_image(url_des, title, intro)
        return True

    except Exception as e:
        print(f"Loi {e}")


def handle():
    name = platform.node()
    print(name)
    if name == "funpic":
        links_df = pd.read_csv("funpic.csv", encoding='unicode_escape', engine='python')
        links_df['intro'] = "funpic"
    elif name == "smile":
        links_df = pd.read_csv("smile.csv", encoding='unicode_escape', engine='python')
        links_df['intro'] = "smile"
    elif name == "dailyjoy":
        links_df = pd.read_csv("dailyjoy.csv", encoding='unicode_escape', engine='python')
        links_df['intro'] = "dailyjoy"
    elif name == "findingjoy":
        links_df = pd.read_csv("findingjoy.csv", encoding='unicode_escape', engine='python')
        links_df['intro'] = "findingjoy"
    elif name == "happymonkey":
        links_df = pd.read_csv("happymonkey.csv", encoding='unicode_escape', engine='python')
        links_df['intro'] = "happymonkey"
    else:
        FILES = ["funpic", "smile", "dailyjoy", "findingjoy", "happymonkey"]

        links_df = pd.DataFrame({"STT": [], "Title": [], "Link": [], "intro": []})
        for file in FILES:
            try:
                df = pd.read_csv(f"{file}.csv", encoding='unicode_escape', engine='python')
                df.columns = ['STT', 'Title', 'Link']
                df['intro'] = file
                print(df['Title'])
                links_df = links_df.append(df, ignore_index=True)
            except Exception as e:
                print(f"mo file loi {e}")
                continue

    links_df = links_df.sort_values(by=['STT'])
    loop_df(links_df)



def loop_df(df):
    for index, row in df.iterrows():
        reup_df = pd.read_csv("reup_list.csv", encoding='unicode_escape', engine='python')
        stt = row['STT']
        title = row['Title']
        link = row['Link']
        intro = row['intro']
        if (intro + " " + link) in reup_df["LINK"].to_list():
            print(f"Link {link} da render")
            continue
        print(f"Render link {link}")
        if (gen_video(stt, title, link, intro)):
            print(intro)
        reup_df = reup_df.append(pd.DataFrame({"LINK": [intro + " " + link]}))
        reup_df["LINK"].to_csv("reup_list.csv", index=False)


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
os.system("zip -r videos.zip /home/vuhaibangtk/videos/*")
os.system("mv videos.zip /home/vuhaibangtk/videos")
while True:
    if update_repo():
        handle()
        import glob
        if (glob.glob("/home/vuhaibangtk/videos/*.mp4")):
            os.system("zip -r videos.zip /home/vuhaibangtk/videos/*")
            os.system("mv videos.zip /home/vuhaibangtk/videos")
    time.sleep(60*5)

