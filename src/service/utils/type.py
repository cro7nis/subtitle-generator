from typing import Dict, Union, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class ASRResult(BaseModel):
    transcription: Optional[str] = None
    word_hyp: Optional[List[str]] = None
    word_ts_hyp: Optional[List[Tuple[float, float]]] = None
    processing_duration: Optional[float] = 0.0
    language: Optional[str] = None
    raw_result: Optional[Union[Dict, List[Dict]]] = None


class Format(str, Enum):
    txt = "txt"
    vtt = "vtt"
    srt = "srt"
    tsv = "tsv"
    json = "json"


class Task(str, Enum):
    transcribe = "transcribe"
    translate = "translate"


class Request(BaseModel, use_enum_values=True):
    url: str
    language: Optional[str] = None
    outputDir: Optional[str] = None
    format: Format = Format.srt
    task: Task = Task.transcribe


class LanguageResult(BaseModel):
    language: str
    probability: float
    predictions: Optional[dict] = None


class NotFoundResponse(BaseModel):
    error: str = 'Not found'
    message: str
    code: int = 404


class ServerErrorResponse(BaseModel):
    error: str = 'Internal Server Error'
    message: str
    code: int = 500


class BadRequestResponse(BaseModel):
    error: str = 'Bad request'
    message: str
    code: int = 400


class SystemInfo(BaseModel):
    torch_version: str
    torch_cuda_available: bool
    torch_cuda_version: Optional[str] = None


class ServerInfo(BaseModel):
    worker_class: str
    workers: int
    bind: int
    timeout: int


class Info(BaseModel):
    server_info: ServerInfo
    system_info: SystemInfo


class HealthStatus(BaseModel):
    status: str = 'UP'


URI_VAL = 'uri'
CLASS_VAL = 'class'
OptionDict = Dict[str, Union[str, int]]

LANGUAGES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
}
