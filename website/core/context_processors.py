from django.conf import settings

def base_url(request=None):
    """
    Return the URL where the server run, based on settings
    """
    return {'BASE_URL': settings.BASE_URL}
