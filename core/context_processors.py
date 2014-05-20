from django.conf import settings

def server_endpoint(request):
    return {'SERVER_ENDPOINT': settings.SERVER_ENDPOINT}
