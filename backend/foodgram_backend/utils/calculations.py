from recipes.models import Subscribe


def is_subscribed(obj1, obj2):
    return Subscribe.objects.filter(user=obj1, author=obj2).exists()
