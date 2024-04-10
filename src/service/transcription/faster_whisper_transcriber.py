import os
from timeit import default_timer as timer
from typing import Optional

import faster_whisper
import torch
from faster_whisper.audio import decode_audio
from faster_whisper.utils import download_model, available_models

from service.transcription.transcriber import Transcriber
from service.utils.file import unpack
from service.utils.type import ASRResult, LanguageResult


class FasterWhisperTranscriber(Transcriber):

    def __init__(self, cfg):
        super(FasterWhisperTranscriber, self).__init__(cfg)
        self.ckpt_downloaded = False
        self.save_dir = os.path.join(self.cfg.ckpt_path, self.cfg.model)
        self.download_whisper_checkpoint()
        self.name = 'FasterWhisperTranscriber'
        self.device = None

    def initialize_model(self) -> None:
        self.device = self.get_device()
        device_index = 0
        if ':' in self.device:
            device, device_index = self.device.split(':')
            device_index = int(device_index)
        else:
            device = self.device
        if self.device == 'cpu':
            if self.cfg.compute_type not in ['float32', 'int8']:
                self.logger.warning(f'{self.cfg.compute_type} not supported for cpu. Changing to float32')
                self.cfg.compute_type = 'float32'
        self.model = faster_whisper.WhisperModel(self.cfg.model, download_root=self.save_dir, device=device,
                                                 device_index=device_index,
                                                 compute_type=self.cfg.compute_type,
                                                 local_files_only=self.cfg.local_files_only,
                                                 num_workers=self.cfg.num_workers,
                                                 cpu_threads=self.cfg.cpu_threads)
        self.logger.info(f'Model is running on {self.device}')
        self.loaded = True

    def assert_checkpoint_is_downloaded(self):
        if not self.cfg.local_files_only:
            if not self.ckpt_downloaded:
                raise Exception('Checkpoint is still downloading. Please try again in a while')

    def download_whisper_checkpoint(self):
        if not self.cfg.local_files_only:
            if self.cfg.model in available_models():
                self.logger.info(f'Checking if ckpt exists exists in {self.save_dir}. If not it will download it')
                download_model(f'Systran/faster-whisper-{self.cfg.model}',
                               local_files_only=self.cfg.local_files_only,
                               cache_dir=self.save_dir)
                self.ckpt_downloaded = True

            else:
                raise RuntimeError(
                    f"Model {self.cfg.model} not found; available models = {available_models()}"
                )

    def transcribe(self, audio_file: str, language: str = None, task: str = 'transcribe', speaker_labels: list = None,
                   available_languages=None,
                   language_mode: Optional[str] = 'suggest'):
        assert task in ['transcribe', 'translate']
        result = self.transcribe_full_audio(audio_file, language=language, task=task)
        if 'cuda' in self.device:
            torch.cuda.empty_cache()
        return result

    def get_parameters(self):
        return {'model': self.cfg.model,
                'mode': self.cfg.mode,
                'beam_size': self.cfg.parameters.beam_size,
                'condition_on_previous_text': self.cfg.parameters.condition_on_previous_text,
                'temperature': self.cfg.parameters.temperature
                }

    def transcribe_full_audio(self, audio_file: str, language: str = None, task: str = 'transcribe') -> ASRResult:
        self.assert_checkpoint_is_downloaded()
        self.load_model_if_not_loaded()
        start = timer()
        audio = decode_audio(audio_file)
        segments, info = self.model.transcribe(audio, language=language, task=task, **self.cfg.parameters)
        segments = list(segments)
        segments = unpack(segments)
        asr_result = {'segments': segments, 'language': info.language}
        language = asr_result['language']

        if self.cfg.parameters.word_timestamps:
            words = []
            for i in asr_result['segments']:
                words.extend(i['words'])
            word_hyp = [i['word'] for i in words]
            word_ts_hyp = [[i['start'], i['end']] for i in words]
            transcription = ' '.join([segment['text'] for segment in asr_result['segments']]).strip()
        else:
            transcription = ' '.join([segment['text'] for segment in asr_result['segments']]).strip()
            word_hyp = None
            word_ts_hyp = None

        end = timer()
        processing_duration = end - start

        if 'cuda' in self.cfg.device:
            torch.cuda.empty_cache()

        return ASRResult(transcription=transcription, word_hyp=word_hyp, word_ts_hyp=word_ts_hyp,
                         processing_duration=processing_duration,
                         language=language, raw_result=asr_result)

    def detect_language(self, audio, fallback_language=None) -> LanguageResult:

        features = self.model.feature_extractor(audio)
        segment = features[:, : self.model.feature_extractor.nb_max_frames]
        encoder_output = self.model.encode(segment)
        results = self.model.model.detect_language(encoder_output)[0]
        # Parse language names to strip out markers
        probs = {token[2:-2]: prob for (token, prob) in results}
        languages = sorted(probs.items(), key=lambda kv: kv[1])[::-1]
        language, probability = languages[0]
        top_three_predictions = {lang[0]: lang[1] for lang in languages[:3]}
        return LanguageResult(language=language, probability=probability, predictions=top_three_predictions)
