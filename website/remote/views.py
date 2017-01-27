from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Device


class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            device = self.create_device(user)
            return JsonResponse({'data': device.token})
        else:
            return JsonResponse({'error': 'Wrong credentials'})

    def create_device(self, user):
        device = Device(user=user)
        device.save()
        print(device.token)
        return device
