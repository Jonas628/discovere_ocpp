from asgiref.sync import sync_to_async


@sync_to_async
def save_object(object):
    object.save()