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
        title = f"Fun Pic: Step {stt} {title}"
        # print(link)
        # print(len(url_des))
        # for url in url_des:
        #     print(url)
        gen_video_from_url_image(url_des, title)
    except Exception as e:
        print(f"Loi {e}")


def handle():
    t = time.time()
    links_df = pd.read_csv("day1.csv")
    if platform.node() == "machine1":
        links_df = links_df[:int(len(links_df)/3)]
    elif platform.node() == "machine2":
        links_df = links_df[int(len(links_df) / 3):int(len(links_df) * 2 / 3)]
    elif platform.node() == "machine3":
        links_df = links_df[int(len(links_df)*2/3):]
    else:
        pass
    for index, row in links_df.iterrows():
        stt = row['STT']
        title = row['Title']
        link = row['Link']
        gen_video(stt, title, link)
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

