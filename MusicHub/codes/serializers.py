from rest_framework import serializers

from MusicHub.codes.constants import CODE_LENGTH


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=CODE_LENGTH, allow_null=False)
