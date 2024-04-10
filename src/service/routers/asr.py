import os
import traceback
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from service.configs import settings
from loguru import logger

from service.transcription.faster_whisper_transcriber import FasterWhisperTranscriber
from service.transcription.utils.subtitle import get_writer
from service.utils.signal import read_signal
from service.utils.type import Request, LANGUAGES
from fastapi.responses import FileResponse

from service.utils.youtube import get_audio_from_youtube_video

router = APIRouter(
    prefix=settings.api.endpoints.prefix,
    tags=["subtitles"],
    dependencies=None,
)

transcriber = FasterWhisperTranscriber(settings.transcriber)


@router.post('/' + settings.api.endpoints.asr)
async def asr(request: Request):
    url = request.url
    output_dir = request.outputDir if request.outputDir is not None else settings.output_dir
    task = request.task
    fmt = request.format
    language = request.language
    os.makedirs(output_dir, exist_ok=True)
    requestId = str(uuid4())
    logger.debug(f'Setting random ID: {requestId}')

    try:
        path = get_audio_from_youtube_video(url)
    except Exception as e:
        error = traceback.format_exc().splitlines()[-1]
        logger.error(f'Error with youtube download: {error} for request {requestId}')
        raise HTTPException(status_code=400, detail=f'Error with youtube download: {error}')

    if language is not None:
        if language.lower() == 'auto':
            language = None
        elif language not in LANGUAGES:
            logger.error(f'{language} should be in one of the following: {list(LANGUAGES.keys())}')
            raise HTTPException(status_code=400,
                                detail=f'{language} should be in one of the following: {list(LANGUAGES.keys())}')

    audio_name = os.path.basename(path).split('.')[0]
    logger.debug(f'audio_name: {audio_name}')
    logger.info(f'New request. ID: {requestId}, Path: {path}')
    logger.debug(f'Request: {request}')

    if os.path.exists(path):
        try:
            signal, sr, duration = read_signal(path, sr=None, plot=False, log=False)
            logger.info(f'Audio duration: {duration:.2f}, sampling rate: {sr} for request with ID: {requestId}')
            language = None if task == 'translate' else language
            result = transcriber.transcribe(path, language=language, task=task)
            os.remove(path)
            writer = get_writer(fmt, output_dir)
            writer(result.raw_result, os.path.join(output_dir, requestId + '.' + fmt))
            return FileResponse(os.path.join(output_dir, requestId + '.' + fmt), media_type='text/plain')
        except Exception as e:
            error = traceback.format_exc().splitlines()[-1]
            logger.error(error)
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong. "
                                       f"More details: {error} ")
    else:
        logger.error(f'{path} file not found for request {requestId}')
        raise HTTPException(status_code=400, detail=f'{path}  file not found')
