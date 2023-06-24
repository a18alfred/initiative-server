from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file(image):
    file_size = image.size
    if file_size > settings.SAVED_PICTURE_MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError("Максимальный размер файла %s MB" % settings.SAVED_PICTURE_MAX_FILE_SIZE_MB)
