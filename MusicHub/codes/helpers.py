from MusicHub.main.exception_handler import CustomException


def get_or_400(model, *args, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise CustomException("Could not find object with given attributes")
