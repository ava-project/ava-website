import base64

from .models import Device


class BasicAuthRemote(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def get_user_token(self, email, token):
        try:
            device = Device.objects.get(token=token)
            if device.user.email != email:
                return None
            return device.user
        except Device.DoesNotExist:
            return None

    def __call__(self, req):
        if not req.user.is_authenticated and 'HTTP_AUTHORIZATION' in req.META:
            auth = req.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                from_header = base64.b64decode(auth[1]).decode('utf-8')
                email, token = from_header.split(':')
                user = self.get_user_token(email, token)
                if user:
                    req.user = user
        return self.get_response(req)
