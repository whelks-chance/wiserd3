from wiserd3 import settings


def is_dev_processor(request):
    return {'is_dev': settings.IS_DEV}
