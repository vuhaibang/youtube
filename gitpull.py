import git
import time


while True:
    g = git.cmd.Git()
    g.pull()
    time.sleep(120)