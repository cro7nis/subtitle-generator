from typing import Optional

import librosa
import numpy as np
import logging
from loguru import logger
import os


def convert_2_wav(input_path, audio_path, sample_rate=16000, log=False):
    import subprocess
    # convert a file from mp3/mp4 to wav mono 16KHz
    flag = '-loglevel quiet' if not log else ''
    command = f'ffmpeg -i {input_path} -y -ar {sample_rate} -ac 1 {audio_path} ' + flag
    result = subprocess.call(command, shell=True)


def read_signal(path, sr=Optional[int], plot=False, log=False, mono=False):
    name = path.split('/')[-1]
    signal, sr = librosa.load(path, sr=sr, mono=mono)
    duration = librosa.get_duration(y=signal, sr=sr)
    if log:
        logging.info(f'Duration of audio is {duration} seconds')
    if plot:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)
        fig.set_figwidth(20)
        fig.set_figheight(2)
        plt.plot(np.arange(len(signal)), signal, 'gray')
        fig.suptitle(name + ' audio', fontsize=16)
        plt.xlabel('time (secs)', fontsize=18)
        ax.margins(x=0)
        plt.ylabel('signal strength', fontsize=16);
        a, _ = plt.xticks();
        plt.xticks(a, a / sr);
    return signal, sr, duration


def sanitize_audio(path, target_sr, target_channels, correlationId):
    signal, sr, duration = read_signal(path, sr=None, plot=False, log=False)
    if signal.ndim > target_channels or int(sr) != int(target_sr):
        if signal.ndim > target_channels:
            logger.info(f'{correlationId} audio file has {signal.shape[0]} channels')
        if sr != target_sr:
            logger.info(f'{correlationId} audio file has {sr} sampling rate')
        audio_filename = os.path.basename(path).split('.')[0]
        new_path = path.replace(audio_filename, audio_filename + '_sanitized')
        logger.info(f'Converting {correlationId} audio file')
        convert_2_wav(path, new_path, sample_rate=target_sr)
        os.rename(path, path.replace(audio_filename, audio_filename + '_original'))
        os.rename(new_path, path)
        signal, sr, duration = read_signal(path, sr=None, plot=False, log=False)
        logger.info(
            f'Converted audio duration: {duration:.2f}, sampling rate: {sr} for request with ID: {correlationId}')
