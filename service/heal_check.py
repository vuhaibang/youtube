import psutil
import time
import platform
import pandas as pd
import os

def check_heal():
    reup_df = pd.read_csv("reup_list.csv")
    if platform.node() == "funpic":
        links_df = pd.read_csv("funpic.csv")
        links_df['intro'] = "fun_pic"
    elif platform.node() == "smile":
        links_df = pd.read_csv("smile.csv")
        links_df['intro'] = "smile"
    else:
        FILES = ["funpic", "smile", "dailyjoy", "finfingjoy", "spreadinglaughter"]

        links_df = pd.DataFrame({"STT": [], "Title": [], "Link": [], "intro": []})
        for file in FILES:
            try:
                df = pd.read_csv(f"{file}.csv")
                df['intro'] = file
                links_df = links_df.append(df, ignore_index=True)
            except:
                pass
        for index, row in links_df.iterrows():
            link = row['Link']
            intro = row['intro']
            if (intro + " " + link) in reup_df["LINK"].to_list():
                continue
            else:
                print(f"Link {link} chua co")
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


