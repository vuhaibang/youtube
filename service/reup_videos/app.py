import moviepy.editor as mpe


def add_audio_in_videos(path_video, path_audio, path_output):
    my_clip = mpe.VideoFileClip(path_video)
    audio_background = mpe.AudioFileClip(path_audio)
    final_audio = my_clip.set_audio(audio_background)
    final_audio.write_videofile(path_output)


