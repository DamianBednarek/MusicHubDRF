from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import (
    EmailValidator,
    FileExtensionValidator,
    RegexValidator,
)
from django.db import models

from MusicHub.main.constants import NAME_REGEX, PASSWORD_REGEX, ValidationMessage
from MusicHub.main.metaModel import Meta


class CustomManager(BaseUserManager):
    def create_user(self, email: str, password: str, first_name: str, last_name: str, **kwargs):
        """
        Creates and saves a User with a given email and password.
        """
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, first_name: str, last_name: str, **kwargs):
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **kwargs
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)

        return user

    def get_queryset_verified(self):
        return super(CustomManager, self).get_queryset().filter(is_verified=True)


class User(AbstractBaseUser, Meta):
    first_name = models.CharField(max_length=30, blank=False, null=False,
                                  validators=[RegexValidator(regex=NAME_REGEX, message=ValidationMessage.NAME)]
                                  )
    last_name = models.CharField(max_length=30, blank=False, null=False,
                                 validators=[RegexValidator(regex=NAME_REGEX, message=ValidationMessage.NAME)]
                                 )
    email = models.EmailField(verbose_name="email address", unique=True, max_length=256,
                              validators=[EmailValidator(code="Invalid email", message=ValidationMessage.EMAIL)]
                              )
    password = models.CharField(max_length=100,
                                validators=[RegexValidator(regex=PASSWORD_REGEX, message=ValidationMessage.PASSWORD)]
                                )
    profile_avatar = models.ImageField("Avatar", upload_to="users/avatar", blank=True, null=True,
                                       validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])]
                                       )
    followers = models.ManyToManyField("users.User", blank=True, symmetrical=False)

    is_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def __str__(self):
        return self.email

    def get_email_short(self) -> str:
        """
        Get first part of email example:
        for example@mail.com will return example
        """
        return self.email.split("@")[0]
