import moviepy.editor as mpe
import os


def add_audio_in_videos(path_video, path_audio, path_output):
    my_clip = mpe.VideoFileClip(path_video)
    audio_background = mpe.AudioFileClip(path_audio)
    final_audio = my_clip.set_audio(audio_background)
    final_audio.write_videofile(path_output)


def generator_videos_from_images(dir_path):
    pass


dir_path = '../../images/brightside.me/6 Gym Exercise Alternatives You Can Do at Home'
list_images = sorted(os.listdir(dir_path))
list_images = [os.path.join(dir_path, l) for l in list_images]
clips = [mpe.ImageClip(m).set_duration(3) for m in list_images]
concat_clip = mpe.concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("test.mp4", fps=30)
