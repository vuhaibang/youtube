import moviepy.editor as mpe
import os
import sqlite3
import random
import numpy as np
from moviepy.config import change_settings
if os.path.isdir("/home/vhb/Downloads/"):
    change_settings({"IMAGEMAGICK_BINARY": r"/home/vhb/Downloads/magick"})
elif os.path.isfile("/home/vuhaibangtk/Downloads/magick"):
    change_settings({"IMAGEMAGICK_BINARY": r"/home/vuhaibangtk/Downloads/magick"})
elif os.path.isfile("/home/vuhaibangtk/youtube/magick"):
    change_settings({"IMAGEMAGICK_BINARY": r"/home/vuhaibangtk/youtube/magick"})


def select_sqlite(table, value, conn):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE id=(?)", ([value]))
    row = cur.fetchall()
    cur.close()
    return row[0]

def cascade(screenpos, i):
    v = np.array([0, -1])
    d = lambda t: 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))
    return lambda t: screenpos + v * 400 * d(t - 0.15 * i)


def arrive(screenpos, i):
    v = np.array([-1, 0])
    d = lambda t: max(0, 3 - 3 * t)
    return lambda t: screenpos - 400 * v * d(t - 0.2 * i)


def add_audio_in_videos(path_video, path_audio, path_output):
    my_clip = mpe.VideoFileClip(path_video)
    audio_background = mpe.AudioFileClip(path_audio)
    final_audio = my_clip.set_audio(audio_background)
    final_audio.write_videofile(path_output, fps=30, codec='libx264')


def replace_space_in_text(text):
    text = text.replace("\n", " ")
    if len(text) < 50:
        return 1, text
    result = []
    while len(text) > 50:
        index_space = text[:50].rfind(" ")
        result.append(text[:index_space])
        text = text[index_space+1:]
    if len(text) > 10:
        result.append(text)
    line_text = len(result)
    result = "\n".join(result)
    result = result.capitalize()
    return line_text, result


def resize_center_image_in_video(image_w, image_h, w, h):
    image_w = max(int(image_w * h/ image_h), int(w/2))
    image_h = h
    return (image_w, image_h)


def gen_video_from_url_image(url_deses, title_video, screensize = (1920, 1080)):
    if os.path.isdir('/home/vuhaibangtk/'):
        audio_path = '/home/vuhaibangtk/youtube/audio'
        path_video_out_put = f'/home/vuhaibangtk/videos/{title_video}.mp4'
        path_intro = f'/home/vuhaibangtk/youtube/videos/intro/fun_pic.mp4'
        bottom_path = "/home/vuhaibangtk/youtube/service/reup_videos/bottom.png"
    elif os.path.isdir('/home/vhb/'):
        audio_path = '/home/vhb/PycharmProjects/Project/youtube/audio'
        path_video_out_put = f'/home/vhb/PycharmProjects/Project/videos/{title_video}.mp4'
        path_intro = '/home/vhb/PycharmProjects/Project/youtube/videos/intro/fun_pic.mp4'
        bottom_path = "/home/vhb/PycharmProjects/Project/youtube/service/reup_videos/bottom.png"
    else:
        audio_path = 'C:/Project//youtube/audio'
        path_video_out_put = f'C:/Project/youtube/{title_video}.mp4'
        path_intro = 'C:/Project/youtube/videos/intro/fun_pic.mp4'
        bottom_path = "C:/Project/youtube/service/reup_videos/bottom.png"

    clips = []
    for url, des in url_deses:
        duration = min(11, max(6, len(des)*7/50))
        if len(des) < 1:
            des = "Funy picture"
        line_text, text = replace_space_in_text(des)
        if line_text == 1:
            size_text = int(screensize[0] / 30)
        else:
            size_text = int(screensize[0] / 40)

        try:
            main_image = mpe.ImageClip(url).set_position(('center', 'center')).set_duration(duration)
            back_ground_image = mpe.ImageClip(url).resize(screensize).set_duration(duration).set_opacity(0.5)
            txt_mask = mpe.TextClip(text, font='Amiri-Bold', color='black', fontsize=size_text)
            bottom_image = mpe.ImageClip(bottom_path).resize((screensize[0], line_text * size_text + int(screensize[0]/80)))\
                .set_duration(duration).set_position("bottom", "center")
            txt_mask = txt_mask.set_duration(duration).set_position(("center", screensize[1] - bottom_image.h + int((bottom_image.h - txt_mask.h)/2)))
            main_image = main_image.resize(
                resize_center_image_in_video(main_image.w, main_image.h, screensize[0], screensize[1] - bottom_image.h))\
                .set_position(("center", "top"))
            clip = mpe.CompositeVideoClip([back_ground_image, main_image, bottom_image, txt_mask])
            clip.get_frame(12)
        except:
            continue
        clips.append(clip)
    clips.append(clip.set_duration(7))

    slided_clips = []
    for num, clip in enumerate(clips):
        if num + 1 < len(clips):
            slided_clips.append(mpe.CompositeVideoClip(
                [clips[num + 1].set_start(clip.duration - 2), clip.fx(mpe.transfx.slide_out, 2, 'left')]))
        else:
            slided_clips.append(clip)
    slided_clips.insert(0, mpe.VideoFileClip(path_intro))


    concat_clip = mpe.concatenate_videoclips(slided_clips, method="compose").resize(screensize)
    list_audio = os.listdir(audio_path)
    list_audio = [os.path.join(audio_path, l) for l in list_audio]
    path_audio = random.choice(list_audio)
    audio = mpe.AudioFileClip(path_audio)
    audio = mpe.afx.audio_loop(audio, duration=concat_clip.duration)
    audio = mpe.CompositeAudioClip([mpe.VideoFileClip(path_intro).audio,
                            audio.set_start(mpe.VideoFileClip(path_intro).duration)])
    concat_clip = concat_clip.set_audio(audio).subclip(12, 16)

    concat_clip.write_videofile(path_video_out_put, fps=1, codec='libx264')
if __name__ == '__main__':
    conn_brightside = sqlite3.connect('./../../database/brightside.db')
    add_audio_in_videos("../../videos/videos/St319/1.mp4", "../../videos/audio/St319/1.mp4", "test.mp4")