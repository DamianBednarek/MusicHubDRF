from mutagen import aac, mp3, wave
from pydantic import ValidationError

from MusicHub.main.constants import MAX_FILE_SIZE_IN_MB


def get_track_length(file):
    filename = file.name.split(".")[-1]
    if filename == "mp3":
        return int(mp3.MP3(file).info.length)
    if filename == "wav":
        return int(wave.WAVE(file).info.length)
    if filename == "aac":
        return int(aac.AAC(file).info.length)


def validate_track(data):
    if data.size >= MAX_FILE_SIZE_IN_MB:
        raise ValidationError("File cannot be bigger than 30 Mb")
    # scanner = AntivirusScan(data.name)
    # scanner.scan_file_for_malicious_content(data)


def remove_from_liked_when_set_to_private(instance, validated_data):
    if not validated_data["playlist"].is_public:
        instance.likes.clear()
