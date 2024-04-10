from pytube import YouTube


def get_audio_from_youtube_video(link, max_length=1200):
    yt = YouTube(link)
    youtube_id = yt.vid_info['videoDetails']['videoId']
    if yt.length > max_length:
        raise Exception(f'Video is longer than {max_length} seconds')
    path = yt.streams.filter(only_audio=True)[0].download(filename=f"{youtube_id}.mp3")
    return path
