from django.core.validators import MaxLengthValidator


def MaxLengthValidatorMessage(limit_value):
    return MaxLengthValidator(
        limit_value,
        message=f'Длина не более {limit_value} знаков')
