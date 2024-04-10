from service.utils.youtube import get_audio_from_youtube_video


def test_youtube_dl():
    url = 'https://www.youtube.com/watch?v=1aA1WGON49E&ab_channel=TEDxTalks'
    print(get_audio_from_youtube_video(url))
