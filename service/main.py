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




def gen_video(stt, title, link):
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
        for url in url_des:
            print(url, "\n")
        gen_video_from_url_image(url_des, title)
        return True

    except Exception as e:
        print(f"Loi {e}")


def handle():
    t = time.time()
    if platform.node() == "funpic":
        links_df = pd.read_csv("funpic.csv")
    elif platform.node() == "smile":
        links_df = pd.read_csv("smile.csv")
    else:
        links_df = pd.read_csv("funpic.csv")
    for index, row in links_df.iterrows():
        reup_df = pd.read_csv("reup_list.csv")
        stt = row['STT']
        title = row['Title']
        link = row['Link']
        if link in reup_df["LINK"].to_list():
            continue
        if (gen_video(stt, title, link)):
            reup_df = reup_df.append(pd.DataFrame({"LINK": [link]}))
            reup_df["LINK"].to_csv("reup_list.csv", index=False)
    print(f"Tong time {time.time() - t} s")


handle()
while True:
    repo = git.Repo()
    commit = repo.commit()
    g = git.cmd.Git()
    g.pull()
    if commit != repo.commit():
        print("Change")
        handle()
    else:
        print("No change")
        time.sleep(120)

