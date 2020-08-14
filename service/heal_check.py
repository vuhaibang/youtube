import psutil
import time
import platform
import pandas as pd
import os

def check_heal():
    if platform.node() == "funpic":
        links_df = pd.read_csv("funpic.csv")
    elif platform.node() == "smile":
        links_df = pd.read_csv("smile.csv")
    else:
        links_df = pd.read_csv("funpic.csv")
    for index, row in links_df.iterrows():
        reup_df = pd.read_csv("reup_list.csv")
        link = row['Link']
        if link in reup_df["LINK"].to_list():
            continue
        else:
            return "nok"
    return "ok"


def check_percent_memory():
    if psutil.virtual_memory().percent < 25:
        return True
    else:
        return False


while True:
    status = 'ok'
    if not check_percent_memory():
        status = 'nok'
        for i in range(5):
            if check_percent_memory():
                time.sleep(60)
                continue
            else:
                status = 'ok'

    if status == 'ok':
        time.sleep(60*5)
    else:
        if check_heal() == 'nok':
            print("Su dung tinh nang")
            os.system('tmux attach-session -t reup \; send-key "python3 /home/youtube/service/main.py" Enter')
    time.sleep(60*10)


