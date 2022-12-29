from django.db import models


def clean_word(word):
    return word.lower().replace('ё', 'е')


class LowerCaseEmailField(models.EmailField):
    def get_prep_value(self, value):
        return value.lower()
