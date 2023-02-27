# Generated by Django 4.1 on 2023-01-16 08:46

import MusicHub.main.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9][a-zA-Z0-9\\s\\,\\.\\-]*$')])),
                ('is_public', models.BooleanField(default=True)),
                ('playlist_image', models.ImageField(blank=True, default='playlist/default/default.jpg', null=True, upload_to=MusicHub.main.utils.get_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=models.SET(MusicHub.main.utils.get_sentinal_user), to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='playlist_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
