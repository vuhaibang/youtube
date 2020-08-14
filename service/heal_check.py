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
    a = psutil.cpu_percent(interval=2)
    return a

while True:
    status = 'ok'
    if check_percent_memory() < 40:
        print(f"CPU lower {check_percent_memory()}")
        status = 'nok'
        for i in range(10):
            if check_percent_memory() < 40:
                print(f"Kiem tra lan {i} nok")
                print(f"CPU {check_percent_memory()}")
                time.sleep(15)
                continue
            else:
                status = 'ok'
    else:
        print(f"CPU {check_percent_memory()}")
        print(f"RAM {psutil.virtual_memory().percent}")

    print(f"Tinh trang {status}")
    if status == 'ok':
        pass
    else:
        if check_heal() == 'nok':
            print("Su dung tinh nang")
            os.system('tmux send-keys -t ytb:reup Enter "cd /home/vuhaibangtk/youtube/service" Enter "python3 main.py" Enter')
    time.sleep(60*3)


