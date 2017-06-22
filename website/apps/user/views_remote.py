"""
Django view of the user app.
List of classes:
- RegisterView
- ProfileView
- ProfileEditView
- ValidateTokenEmailView
- ResendValidationEmailView
- RemoteLoginView
- RemoteInfoUserView
- RemoteLogoutView
"""

from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import Device


class RemoteLoginView(View):
    """
    This Endpoint authenticate a user, and create a unique token.
    A client can use Http Basic Auth with email as username and this token as password to sign his requests
    This token expires after two weeks.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            device = Device(user=user)
            device.save()
            return JsonResponse({'data': device.token})
        return JsonResponse({'error': 'Wrong credentials'}, status=400)


class RemoteInfoUserView(View):
    """
    This endpoint returns a json object with user information
    """

    def get(self, request, **kwargs):
        user = request.user
        data = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return JsonResponse(data)


class RemoteLogoutView(View):
    """
    This endpoint logout a user by removing all tokens.
    """

    def get(self, request, **kwargs):
        Device.objects.filter(user=request.user).delete()
        logout(request)
        return JsonResponse({'data': 'You have been logged out'})
