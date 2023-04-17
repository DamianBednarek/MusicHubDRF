import secrets

from django.db import models

from MusicHub.codes.constants import CODE_LENGTH
from MusicHub.config.settings import Common


class CodeManager(models.Manager):
    def create(self, user):
        code = self.model(code=secrets.token_urlsafe(CODE_LENGTH), user=user)
        code.save(using=self._db)
        return code


class SignUpCode(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(to=Common.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CodeManager()


class ResetPasswordCode(SignUpCode):
    pass
