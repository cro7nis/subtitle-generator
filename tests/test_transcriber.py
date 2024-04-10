from service.configs import settings
from service.transcription.faster_whisper_transcriber import FasterWhisperTranscriber
from service.transcription.utils.subtitle import get_writer
from service.utils.logger import logger


def test_transcriber():
    audio_path = 'samples/chunk_1.wav'
    transcriber = FasterWhisperTranscriber(settings.transcriber)
    result = transcriber.transcribe(audio_path)
    logger.info(result.raw_result)
    writer = get_writer('srt', 'outputs/')
    writer(result.raw_result, audio_path)
