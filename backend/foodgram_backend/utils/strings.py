import base64

from django.core.files.base import ContentFile
from django.db import models


def clean_word(word):
    return word.lower().replace('ё', 'е')


class LowerCaseEmailField(models.EmailField):
    def get_prep_value(self, value):
        return value.lower()


def str_to_file(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    name = 'temp.' + ext
    file = ContentFile(base64.b64decode(imgstr), name)
    return (name, file)
